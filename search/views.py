from django.shortcuts import render, redirect
from appointments.models import Appointment
from doctor.models import Doctor
from patient.models import Patient


# Create your views here.
def search(request):
	q = request.GET.get('q')
	qs = Doctor.objects.get_objects(q)
	patient_pk = request.GET.get('patient_pk')

	search_context = {
		'patient_pk': patient_pk,
		'object_list': qs,
		'q': q
	}
	return render(request, "search_q.html", search_context)
