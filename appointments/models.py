from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from patient.models import Patient
from doctor.models import Doctor
from HMS.utils import unique_token_no_generator

User = settings.AUTH_USER_MODEL


class AppointmentManagerQuerySet(models.query.QuerySet):
	def new(self):
		return self.filter(approved=False, disapproved=False, pending=False, done=False)

	def not_new(self):
		lookups = (Q(approved=True) |
				   Q(disapproved=True) |
				   Q(pending=True) |
				   Q(done=True))
		return self.filter(lookups)


class AppointmentManager(models.Manager):
	def get_queryset(self):
		return AppointmentManagerQuerySet(self.model, using=self._db)

	def new(self):
		return self.get_queryset().new()

	def not_new(self):
		return self.get_queryset().not_new()


class Appointment(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

	msg_patient = models.TextField(null=True, blank=True)
	msg_doctor = models.TextField(null=True, blank=True)

	approved = models.BooleanField(default=False)
	disapproved = models.BooleanField(default=False)
	pending = models.BooleanField(default=False)
	done = models.BooleanField(default=False)
	location = models.CharField(max_length=200, null=True, blank=True)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	appointment_date = models.DateField(null=True, blank=True)
	appointment_time = models.TimeField(null=True, blank=True)

	diseases = models.CharField(max_length=300, null=True, blank=True)
	token_no = models.CharField(max_length=55, null=True, blank=True)
	report_generated = models.BooleanField(default=False)
	report = models.FileField(upload_to='reports', null=True, blank=True, verbose_name=' ')

	objects = AppointmentManager()

	def __str__(self):
		return str(self.doctor.full_name) + ' | ' + str(self.patient.full_name)

	def status(self):
		if self.approved:
			return "Approved"
		if self.disapproved:
			return "Disapproved"
		if self.pending:
			return "Pending"
		if self.done:
			return "Done"
		else:
			return "New"

	class Meta:
		ordering = ['-updated', '-created']


def pre_save_token_no(sender, instance, *args, **kwargs):
	if not instance.token_no:
		instance.token_no = unique_token_no_generator(instance)


pre_save.connect(pre_save_token_no, sender=Appointment)

