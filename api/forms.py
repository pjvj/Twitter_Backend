# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django import forms
# from django.core.exceptions import ValidationError
#
#
# class CustomUserCreationForm(forms.Form):
#     name = forms.CharField(label='Enter name',min_length=4, max_length=150)
#     username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
#     password1 = forms.CharField(label='Enter password')
#     password2 = forms.CharField(label='Confirm password')
#
#     def clean_username(self):
#         username = self.cleaned_data['username'].lower()
#         r = UserInfo.objects.filter(username=username)
#         if r.count():
#             raise  ValidationError("Username already exists")
#         return username
#
#     def clean_name(self):
#         name = self.cleaned_data['name'].lower()
#         #r = UserInfo.objects.filter(name=name)
#         #if r.count():
#             #raise  ValidationError("Name already exists")
#         return name
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Password don't match")
#
#         return password2
#
#     def save(self, commit=True):
#         user = UserInfo.objects.create_user(
#             self.cleaned_data['name'],
#             self.cleaned_data['username'],
#             self.cleaned_data['password1']
#         )
#         return user


from .models import UserInfo
from django import forms
class UserRegistrationForm(forms.Form):

    name = forms.CharField(max_length = 50)
    username = forms.CharField(max_length = 50)
    password = forms.CharField(max_length = 50,widget = forms.PasswordInput())

    def save(self, commit=False):
        user = UserInfo.objects.create(
             name=self.cleaned_data['name'],
             username=self.cleaned_data['username'],
             password=self.cleaned_data['password']
        )
        return user
    
