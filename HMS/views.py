from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from .forms import register_form, login_form
from django.contrib import messages
from doctor.models import Doctor
from patient.models import Patient
from chat.models import Message
from django.db.models import Q

User = get_user_model()


def home_page(request):
	form = register_form
	user_type = request.POST.get('user_type')
	if request.method == 'POST':
		user_type = request.POST.get('user_type')
		context = {'form': form, 'user_type': user_type}
		return render(request, 'register.html', context)

	if request.session.get('role') == 'patient':
		patient = Patient.objects.patient(request)
		msgs = patient.message_set.all()
		if msgs:
			request.session['messages'] = True
			request.session['total_messages'] = msgs.filter(from_doctor=True, display=True).count()
			request.session['default_doctor_pk'] = msgs.last().doctor.pk
	if request.session.get('role') == 'doctor':
		doctor = Doctor.objects.doctor(request)
		msgs = doctor.message_set.all()
		if msgs:
			request.session['messages'] = True
			request.session['total_messages'] = msgs.filter(from_patient=True, display=True).count()
			request.session['default_patient_pk'] = msgs.last().patient.pk
	return render(request, 'index.html', {})


def register_page(request):
	form = register_form(request.POST or None)
	if form.is_valid():
		name = form.cleaned_data.get('name')
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		role = form.cleaned_data.get('role')
		new_user = User.objects.create_user(email, password)
		if new_user:
			if role == 'D':
				Doctor.objects.create(doctor_user=new_user, full_name=name, role='doctor')
				msg = """Successfully registered, Please login Now!"""
				messages.success(request, msg)
				return redirect('login')
			elif role == 'P':
				Patient.objects.create(patient_user=new_user, full_name=name, role='patient')
				msg = """Successfully registered, Please login Now!"""
				messages.success(request, msg)
				return redirect('login')
	context = {'form': form}
	return render(request, 'accounts/register.html', context)


def login_page(request):
	doctor_list = Doctor.objects.all()[:3]
	patient_list = Patient.objects.all()[:3]
	form = login_form(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		user = authenticate(request, username=email, password=password)
		if user:
			login(request, user)
			try:
				doctor = Doctor.objects.get(doctor_user=user)
				request.session['pk'] = doctor.pk
				request.session['role'] = 'doctor'
				return redirect('doctor:appointments', slug='requests', doctor_pk=doctor.pk)
			except:
				try:
					patient = Patient.objects.get(patient_user=user)
					request.session['pk'] = patient.pk
					request.session['role'] = 'patient'
					return redirect('patient:patient_account', pk=patient.pk)
				except:
					pass
			return redirect("home")
		else:
			msg = """Invalid Credentials!"""
			messages.success(request, msg)
	context = {
		'form': form,
		'doctor_list': doctor_list,
		'patient_list': patient_list
	}
	return render(request, 'accounts/login.html', context)
