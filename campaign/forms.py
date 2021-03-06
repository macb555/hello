
from django.forms.models import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User as AuthUser

from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.views.generic import CreateView

from django_countries.widgets import CountrySelectWidget

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class DislikeForm(ModelForm):
    class Meta:
        model = Dislike
        fields = ('reason',)

class FeedbackForm(ModelForm):
    class Meta:
        model = Message
        fields = ('email', 'message')


class LoginForm(ModelForm):
    class Meta:
        model = AuthUser
        fields = ('username', 'password')
        password = forms.CharField(widget=forms.PasswordInput())
        #username = forms.CharField(widget=forms.CharField(attrs={'placeholder': 'Enter description here'}))
        widgets = {
            'password': forms.PasswordInput(),
        }
class UserRegistrationForm(ModelForm):
    class Meta:
        model = AuthUser
        fields = ('email', 'first_name', 'last_name','username', 'password')
        password = forms.CharField(widget=forms.PasswordInput)

        widgets = {
            'password': forms.PasswordInput(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mother_name', 'gender', 'marital_status', 'current_country','city_of_residence','region_of_birth','city_of_birth', 'phone_no')
        widgets = {'current_country': CountrySelectWidget()}

class UserInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
    class Meta:
        model = AuthUser
        #password = forms.CharField(widget=forms.PasswordInput)
        #password2 = forms.CharField(widget=forms.PasswordInput)
        fields = ('email','first_name', 'last_name', 'username', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mother_name','gender', 'marital_status', 'phone_no')

class LocationInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('current_country','city_of_residence', 'region_of_birth', 'city_of_birth',)

class VerficationForm(forms.Form):
    verification_code = forms.CharField(label='Verification Code', max_length=100)
    fields = ('verification_code',)

class EmailVerficationForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    verification_code = forms.CharField(label='Verification Code', max_length=100)
    fields = ('email', 'verification_code')
    widgets = {
        'email': forms.EmailInput()
    }

class ForgotPasswordForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    fields = ('email',)
    widgets = {
        'email': forms.EmailInput()
    }

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    fields = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1', None)
        password2 = cleaned_data.get('password2', None)
        if not (password1):
            error_msg = u'This field is required.'
            self._errors['password1'] = self.error_class([error_msg])
        if not (password2):
            error_msg = u'This field is required.'
            self._errors['password2'] = self.error_class([error_msg])
        # password fields must match
        if password1 != password2:
            error_msg = u'Password doesn\'t match the confirmation.'
            self._errors['password1'] = self.error_class([error_msg])
            del cleaned_data['password1']
        return cleaned_data

    widgets = {
        'password1': forms.PasswordInput(),
        'password2': forms.PasswordInput(),
    }
