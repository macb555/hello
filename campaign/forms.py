
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
        password = forms.CharField(widget=forms.PasswordInput)
        #password2 = forms.CharField(widget=forms.PasswordInput)
        fields = ('email','first_name', 'last_name', 'username', 'password')

    '''def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
    def save(self, commit=True):
        user = super(UserInfoForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user'''

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mother_name','gender', 'marital_status',)

class LocationInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('current_country','city_of_residence', 'region_of_birth', 'city_of_birth', 'phone_no',)
