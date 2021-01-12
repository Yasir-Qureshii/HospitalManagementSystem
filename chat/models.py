from django.db import models
from appointments.models import Appointment
from patient.models import Patient
from doctor.models import Doctor
from django.db.models.signals import pre_save, post_save


class Message(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

	msg_patient = models.TextField(null=True, blank=True)
	msg_doctor = models.TextField(null=True, blank=True)

	display = models.BooleanField(default=True)
	from_patient = models.BooleanField(default=False)
	from_doctor = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'Dr: ' + self.doctor.full_name + ' | P: ' + self.patient.full_name

	# class Meta:
	# 	ordering = ['-created']
