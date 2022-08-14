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
    word = forms.CharField(max_length=2000)