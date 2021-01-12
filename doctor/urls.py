from django.conf.urls import url
from .views import (
    doctor_home,
    appointments,
    preview,
    patient_list,
    update_profile,
    respond,
    view_profile,
    create_msg,
    create_appointment,
    download_report,
    GeneratePDF,
    delete_appointment,
    generate_report,
)

app_name = "doctor"

urlpatterns = [
    url(r'^appointments/(?P<doctor_pk>\d+)/(?P<slug>[\w-]+)/$', appointments, name='appointments'),
    url(r'^info/(?P<pk>\d+)/$', preview, name='doctor_preview'),
    url(r'^patients/$', patient_list, name='patient_list'),
    url(r'^update/$', update_profile, name='update'),
    url(r'^respond/(?P<ap_pk>\d+)/$', respond, name='respond'),
    url(r'^send/$', create_msg, name='create_msg'),
    url(r'^profile/$', view_profile, name='view_profile'),
    url(r'^create-appointment/$', create_appointment, name='create_appointment'),
    url(r'^download-report/(?P<ap_pk>\d+)/$', download_report, name='download_report'),
    url(r'^pdf/(?P<ap_pk>\d+)/$', GeneratePDF.as_view(), name='GeneratePDF'),
    url(r'^delete/(?P<ap_pk>\d+)/$', delete_appointment, name='delete_appointment'),
    url(r'^report/(?P<ap_pk>\d+)/$', generate_report, name='generate_report'),
]

# (?P<pk>\d+)
# (?P<slug>[\w-]+)
