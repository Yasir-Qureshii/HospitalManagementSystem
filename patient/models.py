from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


blood_group = [
	('A+', 'A+'),
	('A-', 'A-'),
	('B+', 'B+'),
	('B-', 'B-'),
	('C+', 'C+'),
	('C-', 'C-'),
	('O+', 'O+'),
	('O-', 'O-')
]


class PatientManager(models.Manager):
	def patient(self, request):
		pk = request.session.get('pk')
		return self.get(pk=pk)


class Patient(models.Model):
	patient_user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=25, null=True, blank=True)
	full_name = models.CharField(max_length=100, null=True, blank=True)
	age = models.PositiveIntegerField(null=True, blank=True, default=20)
	weight = models.PositiveIntegerField(null=True, blank=True)
	blood_group = models.CharField(max_length=2, choices=blood_group, null=True, blank=True)
	image = models.ImageField(upload_to='patients', null=True, blank=True)
	diseases = models.CharField(max_length=300, null=True, blank=True)
	phone_number = models.PositiveIntegerField(null=True, blank=True)
	id_card = models.PositiveIntegerField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True)

	objects = PatientManager()

	def __str__(self):
		return self.full_name

