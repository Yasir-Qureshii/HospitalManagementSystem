from django import forms
from .models import Appointment
from django.contrib.auth import authenticate, login, get_user_model
User = get_user_model()


class AppointmentRespondForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Location'}
    ), label='')

    approved = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked': 'True', 'class': 'hide_this', 'style': 'display:none'}), label='')
    pending = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked': 'False', 'class': 'hide_this', 'style': 'display:none'}), label='')

    class Meta:
        model = Appointment
        # fields = ('appointment_date', 'appointment_time', 'location')
        fields = ('appointment_date', 'appointment_time', 'location', 'approved', 'pending')

        widgets = {
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'yyy-mm-dd', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'hr:min', 'type': 'time'}),
            # 'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            # 'msg_doctor': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Message'},),
        }


class UploadReportForm(forms.ModelForm):
    # report = forms.FileField(widget=forms.FileField())

    class Meta:
        model = Appointment
        fields = ('report', )
