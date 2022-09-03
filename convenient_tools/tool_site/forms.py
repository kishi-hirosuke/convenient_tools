from tracemalloc import DomainFilter
from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import re

# お問い合わせ
class InquiryForm(forms.Form):
    name = forms.CharField(
        label='氏名',
        max_length=20,
    )
    name_detail = forms.CharField(
        label='ふりがな',
        max_length=40,
    )
    company = forms.CharField(
        label='会社名',
        max_length=40,
    )
    tel = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        #error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
    )
    mail = forms.EmailField(
        label='メールアドレス',
        required=True,
        max_length=50,
    )
    kinds = forms.ChoiceField(
        label='種類',
        required=True,
        disabled=False,
        choices=[('','種類選択'),('改善提案','改善提案'),('ご質問','ご質問')],
        widget=forms.Select,
    )
    message = forms.CharField(
        label='内容',
        required=False,
        max_length=200,
        widget=forms.Textarea,
    )

# 処理
def file_size(value):
    limit = 500*1000*1000
    if value.size > limit:
        raise ValidationError(f'ファイルサイズが大きすぎます。{limit/1000/1000}MBより小さいサイズにしてください。')

class UploadExtract(forms.Form):
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['csv']),
            file_size
            ]
    )
    columuns = forms.CharField(max_length=255)
    code = forms.CharField(max_length=2000)


class UploadSplit(forms.Form):
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['csv']),
            file_size
            ]
    )
    num = forms.CharField(max_length=255)