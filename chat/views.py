from django.shortcuts import render, redirect
from .models import Message
from doctor.models import Doctor
from patient.models import Patient
from appointments.models import Appointment
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# for doctor message view
@login_required
def message_view(request, patient_pk):
    doctor = Doctor.objects.doctor(request)
    patient = Patient.objects.get(pk=patient_pk)
    # lookup = (Q(disapproved=True) | Q(pending=True))
    appointments = doctor.appointment_set.all().not_new()
    messages = doctor.message_set.filter(patient=patient)

    # for showing messages
    msgs = doctor.message_set.all()
    if msgs:
        request.session['messages'] = True
        request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
        request.session['default_patient_pk'] = msgs.first().patient.pk

    try:
        patient_msgs = Message.objects.filter(patient=patient, doctor=doctor, from_patient=True, display=True)
        patient_msgs_count = patient_msgs.count()
        total_messages = request.session.get('total_messages')
        request.session['total_messages'] = total_messages - patient_msgs_count
        patient_msgs.update(display=False)
    except:
        pass
    patient_name = patient.full_name
    context = {
        'appointments': appointments,
        'patient': patient,
        'messages': messages,
        'patient_name': patient_name,
        'patient_pk': patient_pk,
    }
    return render(request, 'doctor/message.html', context)


# through both patient's  and doctors account
# first time msg will not created here for doctor
@login_required
def create_message(request):
    if request.session.get('role') == 'doctor':
        doctor_pk = request.session.get('pk')
        doctor = Doctor.objects.get(pk=doctor_pk)
        patient_pk = request.POST.get('patient_pk')
        patient = Patient.objects.get(pk=patient_pk)
        msg_doctor = request.POST.get('msg_doctor')
        Message.objects.create(patient=patient, doctor=doctor, msg_doctor=msg_doctor, from_doctor=True)
        return redirect("chat:message_view", patient_pk=patient_pk)

    patient_pk = request.session.get('pk')
    doctor_pk = request.POST.get('doctor_pk')
    patient = Patient.objects.get(pk=patient_pk)
    doctor = Doctor.objects.get(pk=doctor_pk)
    msg_patient = request.POST.get('msg_patient')
    Message.objects.create(patient=patient, doctor=doctor, msg_patient=msg_patient, from_patient=True)
    return redirect("patient:messages", doctor_pk=doctor_pk)


def delete_msg(request, msg_pk):
    msg = Message.objects.get(pk=msg_pk)
    doctor_pk = msg.doctor.pk
    patient_pk = msg.patient.pk
    if request.session.get('role') == 'doctor':
        msg.from_doctor = False
        msg.save()
        return redirect('chat:message_view', patient_pk=patient_pk)
    msg.from_patient = False
    msg.save()
    return redirect('patient:messages', doctor_pk=doctor_pk)
