from django.shortcuts import redirect, reverse, render
from django.db import models
from django.conf import settings
from django.db.models import Q
# from appointments.models import Appointment
# from patient.models import Patient
User = settings.AUTH_USER_MODEL


class Award(models.Model):
	title = models.CharField(max_length=200)

	def __str__(self):
		return self.title


class DoctorManager(models.Manager):
	def doctor(self, request):
		pk = request.session.get('pk')
		return self.get(pk=pk)

	def get_objects(self, query):
		lookups = (
				Q(full_name__icontains=query) |
				Q(category__icontains=query) |
				Q(about__icontains=query)
		)
		return self.get_queryset().filter(lookups)


categories = (
	('Choose Category', 'Choose Category'),
	('Dentist', 'Dentist'),
	('Nephrologist', 'Nephrologist'),
	('Endocrinologist', 'Endocrinologists'),
	('Ophthalmologist', 'Ophthalmologist'),
	('Cardiologist', 'Cardiologist'),
	('Allergist', 'Allergist'),
	('Pediatrician', 'Pediatrician'),
	('Dermatologist', 'Dermatologist'),
)


class Doctor(models.Model):
	doctor_user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=25, null=True, blank=True)
	# don't use 'user' as field name in model it causes issues
	full_name = models.CharField(max_length=100, null=True, blank=True)
	about = models.TextField(null=True, blank=True)
	awards = models.ManyToManyField(Award, blank=True)
	image = models.ImageField(upload_to='doctors', null=True, blank=True)
	category = models.CharField(max_length=33, choices=categories, default='Choose Category')
	address = models.CharField(max_length=400, null=True, blank=True)
	# image will be saved to static/media_root/uploads

	objects = DoctorManager()

	def __str__(self):
		return self.full_name

	# def get_absolute_url(self):
	# 	return reverse('doctor:doctor_preview', kwargs={'pk': self.pk})
