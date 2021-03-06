from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email","username","first_name","last_name","gender","flat_number","address","estate","mobile_number")
