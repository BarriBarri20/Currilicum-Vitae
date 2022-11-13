from django.forms import ModelForm
from django import forms 
from .models import CurriculumVitae


class UploadFileForm(ModelForm):
    title = forms.CharField(max_length=50)
    cv = forms.FileField()
    class Meta:
        model = CurriculumVitae
        fields = ['title','cv']