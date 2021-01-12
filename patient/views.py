from django.shortcuts import render, get_object_or_404, redirect
from .forms import PatientProfileForm
from .models import Patient
from appointments.models import Appointment
from chat.models import Message
from doctor.models import Doctor
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def patient_home(request):
    patient = Patient.objects.patient(request)
    # for showing messages
    messages = patient.message_set.all().filter(from_doctor=True, display=True)
    if messages:
        request.session['messages'] = True
        request.session['total_messages'] = messages.count()
        request.session['default_doctor_pk'] = messages.last().doctor.pk
    return render(request, 'patient/home.html', {})


@login_required
def patient_account(request, pk):
    patient = Patient.objects.get(pk=pk)
    context = {'object': patient}

    # for showing messages
    if request.session.get('role') == 'patient':
        messages = patient.message_set.all()
        if messages:
            request.session['messages'] = True
            request.session['total_messages'] = messages.filter(from_doctor=True, display=True).count()
            request.session['default_doctor_pk'] = messages.last().doctor.pk
    return render(request, 'patient/account.html', context)


@login_required
def update_profile(request):
    patient = Patient.objects.patient(request)
    form = PatientProfileForm(request.POST or None, request.FILES or None, instance=patient)
    if form.is_valid():
        form.save()
        return redirect('patient:patient_account', pk=patient.pk)
    context = {'form': form, 'object': patient}
    return render(request, 'patient/update_profile.html', context)


@login_required
def patient_appointments(request, status):
    patient = Patient.objects.patient(request)
    new_appointments = patient.appointment_set.all().new()
    appointments = patient.appointment_set.all().not_new().filter(done=False)
    past_appointments = patient.appointment_set.all().filter(done=True)

    approved = patient.appointment_set.all().filter(approved=True)
    for appointment in approved:
        if timezone.now().date() > appointment.appointment_date:
            appointment.done = True
            appointment.approved = False
            appointment.save()
    context = {
        'new_appointments': new_appointments,
        'appointments': appointments,
        'past_appointments': past_appointments,
        'status': status
    }
    # for showing messages
    messages = patient.message_set.all().filter(from_doctor=True, display=True)
    if messages:
        request.session['messages'] = True
        request.session['total_messages'] = messages.count()
        request.session['default_doctor_pk'] = messages.last().doctor.pk
    return render(request, 'patient/appointments.html', context)


@login_required
def message_view(request, doctor_pk):
    patient = Patient.objects.patient(request)
    appointments = patient.appointment_set.all().not_new()
    doctor = Doctor.objects.get(pk=doctor_pk)

    # for showing messages
    messages = patient.message_set.all().filter(from_doctor=True, display=True)
    if messages:
        request.session['messages'] = True
        request.session['total_messages'] = messages.count()
        request.session['default_doctor_pk'] = messages.last().doctor.pk

    doctor_msgs = Message.objects.filter(patient=patient, doctor=doctor, from_doctor=True, display=True)
    if doctor_msgs:
        doctor_msgs_count = doctor_msgs.count()
        total_messages = request.session.get('total_messages')
        request.session['total_messages'] = total_messages - doctor_msgs_count
        doctor_msgs.update(display=False)
    doctor_name = doctor.full_name
    messages = Message.objects.filter(patient=patient, doctor=doctor)
    context = {
        'appointments': appointments,
        'patient': patient,
        'messages': messages,
        'doctor_name': doctor_name,
        'doctor_pk': doctor_pk,
    }

    return render(request, 'patient/message.html', context)


@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'patient/doctor_list.html', {'doctor_list': doctors})