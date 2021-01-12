from django import forms
from django.contrib.auth import authenticate, login, get_user_model
User = get_user_model()

role = [('S', 'Select Role'), ('P', 'Patient'), ('D', 'Doctor')]


class register_form(forms.Form):
    role = forms.CharField(max_length=1, label='', widget=forms.Select(choices=role, attrs={'class': 'form-control'}))
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Choose Password'}))
    c_password = forms.CharField(label='', widget=forms.PasswordInput({'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        c_password = data.get('c_password')
        if data.get('role') == 'S':
            raise forms.ValidationError("Please Select a Role")
        if password != c_password:
            raise forms.ValidationError('Passwords does not Match!')
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.all().filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This Email is Already Registered with an account!")
        return email


class login_form(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
