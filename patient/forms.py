from django import forms
from .models import Patient
from django.contrib.auth import authenticate, login, get_user_model
User = get_user_model()


class PatientProfileForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['patient_user', 'full_name', 'role']
        # fields = ('about', 'awards', 'image')

        help_texts = {
            'weight': '(in kgs)',
        }
