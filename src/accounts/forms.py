from django import forms
from django.core.exceptions import ValidationError

class SignupForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=100)
    lastname = forms.CharField(label='LastName', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

class PasswordChangeForm(forms.Form):
    oldpassword = forms.CharField(label='password', max_length=100)
    newpassword1 = forms.CharField(label='new Password', max_length=100)
    newpassword2 = forms.CharField(label='Repeat new password', max_length=100)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)

class UploadProfilePictureForm(forms.Form):

    file = forms.FileField()