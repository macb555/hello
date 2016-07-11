
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
