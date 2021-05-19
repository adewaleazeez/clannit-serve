from django.forms import ModelForm
from app.estate_mgt.models import *


class NewEstateForm(ModelForm):
    class Meta:
        model = Estate
        fields = '__all__'

