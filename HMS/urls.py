from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LogoutView
from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    home_page,
    register_page,
    login_page,
)
from search.views import search

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page, name='home'),
    url(r'^register/$', register_page, name='register'),
    url(r'^login/$', login_page, name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^doctor/', include('doctor.urls', namespace='doctor')),
    url(r'^patient/', include('patient.urls', namespace='patient')),
    url(r'^messages/', include('chat.urls', namespace='chat')),
    url(r'^search/$', search, name='search'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # necessary if you  want to serves media files locally
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
