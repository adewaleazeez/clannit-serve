from django.forms import ModelForm
from .models import NewVistor


class VisitorMgtForm(ModelForm):
    class Meta:
        model = NewVistor
        fields = ['vistor_unique_code']
