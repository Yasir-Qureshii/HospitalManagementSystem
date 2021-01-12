from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import UpdateProfileForm
from appointments.forms import AppointmentRespondForm, UploadReportForm
from appointments.models import Appointment
from chat.models import Message
from django.contrib.auth.decorators import login_required
from .utils import render_to_pdf
from django.template.loader import get_template
from django.utils import timezone

from wsgiref.util import FileWrapper  # this used in django
from mimetypes import guess_type

from .models import Doctor
from patient.models import Patient


# Create your views here.
@login_required
def doctor_home(request):
    doctor = Doctor.objects.doctor(request)
    # for showing messages
    msgs = doctor.message_set.all()
    if msgs:
        request.session['messages'] = True
        request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
        request.session['default_patient_pk'] = msgs.last().patient.pk
    return render(request, 'doctor/appointments.html', {'object': doctor})


@login_required
def download_report(request, ap_pk):
    appointment = Appointment.objects.get(pk=ap_pk)
    filepath = appointment.report.path
    download_obj = 'Report-' + appointment.patient.full_name
    with open(filepath, 'rb') as f:
        wrapper = FileWrapper(f)
        mimetype = 'application/force-download'
        gussed_mimetype = guess_type(filepath)[0]  # filename.mp4
        print('gussed_mimetype', gussed_mimetype)
        if gussed_mimetype:
            mimetype = gussed_mimetype
        response = HttpResponse(wrapper, content_type=mimetype)
        response['Content-Disposition'] = "attachment;filename=%s" % download_obj
        response['X-SendFile'] = str(download_obj)
        return response


@login_required
def appointments(request, slug, doctor_pk,  *args, **kwargs):
    doctor = Doctor.objects.doctor(request)
    appointment_list = doctor.appointment_set.all().new()
    approved_appointments = doctor.appointment_set.all().filter(approved=True)
    disapproved_appointments = doctor.appointment_set.all().filter(disapproved=True)
    pending_appointments = doctor.appointment_set.all().filter(pending=True)
    done_appointments = doctor.appointment_set.all().filter(done=True)
    form = UploadReportForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        ap_pk = request.POST.get('ap_pk')
        appointment = Appointment.objects.get(pk=ap_pk)
        form = UploadReportForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()

    if approved_appointments:
        request.session['approved_appointments'] = True
    else:
        request.session['approved_appointments'] = False
    if disapproved_appointments:
        request.session['disapproved_appointments'] = True
    else:
        request.session['disapproved_appointments'] = False
    if pending_appointments:
        request.session['pending_appointments'] = True
    else:
        request.session['pending_appointments'] = False
    if done_appointments:
        request.session['done_appointments'] = True
    else:
        request.session['done_appointments'] = False

    if request.method == 'POST':
        ap_pk = request.POST.get('ap_pk')
        appointment = Appointment.objects.get(pk=ap_pk)
        form = UploadReportForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()

    approved = doctor.appointment_set.all().filter(approved=True)
    for appointment in approved:
        if timezone.now().date() > appointment.appointment_date:
            appointment.done = True
            appointment.approved = False
            appointment.save()
    done_appointments = doctor.appointment_set.all().filter(done=True)
    context = {
        'slug': slug,
        'object': doctor,
        'appointment_list': appointment_list,
        'approved_appointments': approved_appointments,
        'disapproved_appointments': disapproved_appointments,
        'pending_appointments': pending_appointments,
        'done_appointments': done_appointments,
        'form': form
    }
    # for showing messages
    msgs = doctor.message_set.all()
    print(msgs, msgs)
    if msgs:
        request.session['messages'] = True
        request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
        request.session['default_patient_pk'] = msgs.last().patient.pk
    return render(request, 'doctor/appointments.html', context)


@login_required
def preview(request, pk):
    doctor_obj = Doctor.objects.get(pk=pk)
    if request.session.get('role') == 'patient':
        patient_pk = request.session.get('pk')
        patient_obj = Patient.objects.get(pk=patient_pk)
        appointment_status = None
        appointment = Appointment.objects.filter(patient=patient_obj, doctor=doctor_obj)
        if appointment:
            appointment_status = appointment.first().status()
        return render(request, 'doctor/preview.html', {'object': doctor_obj, 'appointment_status': appointment_status})

    if request.session.get('role') == 'doctor':
        # for showing messages
        msgs = doctor_obj.message_set.all()
        if msgs:
            request.session['messages'] = True
            request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
            request.session['default_patient_pk'] = msgs.last().patient.pk
    return render(request, 'doctor/preview.html', {'object': doctor_obj})


@login_required
def patient_list(request):
    doctor = Doctor.objects.doctor(request)
    done_appointments = doctor.appointment_set.filter(done=True)
    context = {
        'object': doctor,
        'done_appointments': done_appointments
    }
    # for showing messages
    msgs = doctor.message_set.all()
    if msgs:
        request.session['messages'] = True
        request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
        request.session['default_patient_pk'] = msgs.last().patient.pk
    return render(request, 'doctor/patient_list.html', context)


@login_required
def update_profile(request):
    doctor = Doctor.objects.doctor(request)
    form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=doctor)
    if form.is_valid():
        form.save()
        return redirect('doctor:doctor_preview', pk=doctor.pk)
    context = {'form': form, 'object': doctor}
    # for showing messages
    doctor = Doctor.objects.get(pk=request.session.get('pk'))
    msgs = doctor.message_set.all()
    if msgs:
        request.session['messages'] = True
        request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
        request.session['default_patient_pk'] = msgs.last().patient.pk
    return render(request, 'doctor/update_profile.html', context)


def view_profile(request):
    doctor_pk = request.GET.get("doctor_pk")
    doctor = Doctor.objects.get(pk=doctor_pk)
    appointment_status = None
    if request.session.get('role') == 'patient':
        doctor_pk = request.GET.get("doctor_pk")
        doctor = Doctor.objects.get(pk=doctor_pk)
        patient = Patient.objects.patient(request)
        appointment = Appointment.objects.filter(patient=patient, doctor=doctor)
        if appointment:
            appointment_status = appointment.first().status()

    # for showing messages
    if request.session.get('role') == 'doctor':
        doctor = Doctor.objects.doctor(request)
        msgs = doctor.message_set.all()
        if msgs:
            request.session['messages'] = True
            request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
            request.session['default_patient_pk'] = msgs.last().patient.pk
    context = {
        'object': doctor,
        'appointment_status': appointment_status
    }
    return render(request, 'doctor/preview.html', context)


def create_appointment(request):
    msg_patient = request.POST.get('msg_patient')
    patient_pk = request.POST.get('patient_pk')
    doctor_pk = request.POST.get('doctor_pk')
    doctor = Doctor.objects.get(pk=doctor_pk)
    patient = Patient.objects.get(pk=patient_pk)

    Appointment.objects.create(patient=patient, doctor=doctor, msg_patient=msg_patient)
    return redirect('patient:patient_appointments', status='New')


@login_required
def respond(request, ap_pk):
    appointment = Appointment.objects.get(pk=ap_pk)
    # for approve
    form = AppointmentRespondForm(request.POST or None, instance=appointment)
    if form.is_valid():
        if appointment.pending and appointment.approved:
            appointment.pending = False
            appointment.save()
        msg_doctor = "Your Appointment has been Approved"
        Message.objects.create(patient=appointment.patient, doctor=appointment.doctor, msg_doctor=msg_doctor, from_doctor=True)
        form.save()
        return redirect("doctor:appointments", slug='fixed', doctor_pk=appointment.doctor.pk)
    status = request.GET.get('status')
    context = {
        'form': form,
        'appointment': appointment,
        'status': status
    }
    # for showing messages
    doctor = Doctor.objects.doctor(request)
    msgs = doctor.message_set.all()
    if msgs:
        request.session['messages'] = True
        request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
        request.session['default_patient_pk'] = msgs.last().patient.pk
    return render(request, 'doctor/respond.html', context)


def create_msg(request):
    ap_pk = request.POST.get('ap_pk')
    appointment = Appointment.objects.get(pk=ap_pk)
    doctor = appointment.doctor
    patient = appointment.patient
    msg_disapprove = request.POST.get('msg_disapprove')
    msg_info = request.POST.get('msg_info')

    if msg_disapprove:
        Appointment.objects.filter(pk=ap_pk).update(disapproved=True, pending=False)
        msg = Message.objects.create(doctor=doctor, patient=patient, msg_doctor=msg_disapprove, from_doctor=True)
        request.session['messages'] = True
        request.session['default_patient_pk'] = msg.patient.pk
        return redirect("doctor:appointments", slug='disapproved', doctor_pk=appointment.doctor.pk)
    if msg_info:
        Appointment.objects.filter(pk=ap_pk).update(pending=True)
        msg = Message.objects.create(doctor=doctor, patient=patient, msg_doctor=msg_info, from_doctor=True)
        request.session['messages'] = True
        request.session['default_patient_pk'] = msg.patient.pk
        return redirect("doctor:appointments", slug='pending', doctor_pk=appointment.doctor.pk)
    return redirect('/')


def generate_report(request, ap_pk):
    appointment = Appointment.objects.get(pk=ap_pk)
    if request.method == 'POST':
        msg = request.POST.get('msg')
        print()
    context = {
        'patient': appointment.patient,
        'ap_pk': ap_pk
    }
    return render(request, 'doctor/generate_report.html', context)


class GeneratePDF(View):
    def post(self, request, ap_pk, *args, **kwargs):
        msg = request.POST.get('msg')
        template = get_template('doctor/invoice.html')
        appointment = Appointment.objects.get(pk=ap_pk)
        appointment_no = appointment.token_no
        patient = Patient.objects.get(pk=appointment.patient.pk)
        context = {
            "appointment_no": appointment_no,
            "patient": patient,
            "today": timezone.now().date(),
            "appointment_date": appointment.appointment_date,
            "doctor": appointment.doctor,
            "msg": msg
        }
        html = template.render(context)
        pdf = render_to_pdf('doctor/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Medical-Report %s.pdf" %(patient.full_name)
            appointment.report_generated = True
            appointment.save()
            # content = "inline; filename='%s'" %(filename)
            # download = request.POST.get("download")
            # if download:
            #     content = "attachment; filename='%s'" %(filename)
            content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        redirect('doctor:appointments', doctor_pk=appointment.doctor.pk, slug='done')
        return HttpResponse("Not found")


def delete_appointment(request, ap_pk):
    appointment = Appointment.objects.get(pk=ap_pk)
    doctor_pk = appointment.doctor.pk
    Message.objects.filter(doctor=appointment.doctor, patient=appointment.patient).update(from_patient=False, display=False)
    appointment.delete()
    return redirect('doctor:appointments', slug='disapproved', doctor_pk=doctor_pk)
