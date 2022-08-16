from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

class UploadForm(forms.Form):
    testfile = forms.FileField(
        validators=[FileExtensionValidator(['csv'])]
    )
    columuns = forms.CharField(max_length=255)
    code = forms.CharField(max_length=2000)