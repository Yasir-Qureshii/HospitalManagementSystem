from django.conf.urls import url
from .views import patient_account, update_profile, patient_appointments, message_view, doctor_list

app_name = "patient"

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', patient_account, name='patient_account'),
    url(r'^update/$', update_profile, name='update'),
    url(r'^appointments/(?P<status>[\w-]+)/$', patient_appointments, name='patient_appointments'),
    url(r'^messages/(?P<doctor_pk>\d+)/$', message_view, name='messages'),
    url(r'^doctor-list/$', doctor_list, name='doctor_list'),
]
