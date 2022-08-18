from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def file_size(value):
    limit = 20*1000*1000
    if value.size > limit:
        raise ValidationError(f'ファイルサイズが大きすぎます。{limit/1000/1000}MBより小さいサイズにしてください。')

class UploadForm(forms.Form):
    testfile = forms.FileField(
        validators=[
            FileExtensionValidator(['csv']),
            file_size
            ]
    )
    columuns = forms.CharField(max_length=255)
    code = forms.CharField(max_length=2000)