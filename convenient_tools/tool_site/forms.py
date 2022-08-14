from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise ValidationError('※拡張子csvのファイルをアップロードしてください。')

class UploadForm(forms.Form):
    testfile = forms.FileField(
         validators=[validate_file_extension]
    )
    columuns = forms.CharField(max_length=255)
    code = forms.CharField(max_length=2000)