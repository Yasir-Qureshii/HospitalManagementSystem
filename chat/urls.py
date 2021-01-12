from django.conf.urls import url
from .views import (
    create_message,
    delete_msg,
    message_view,
)

app_name = "chat"

urlpatterns = [
    url(r'^new/$', create_message, name='create_message'),
    url(r'^delete/(?P<msg_pk>\d+)/$', delete_msg, name='delete_msg'),
    url(r'^messages/(?P<patient_pk>\d+)/$', message_view, name='message_view'),
]

# (?P<pk>\d+)
# (?P<slug>[\w-]+)
