from django.forms.models import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User

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
        model = User
        fields = ('username', 'password')
        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(),
        }
class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','username', 'password',)
        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(),
        }
