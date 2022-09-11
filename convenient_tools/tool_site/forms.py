from email import header
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
    tel = forms. CharField(
        label='電話番号',
        min_length=9,
        max_length=15,
        widget=forms.TextInput(attrs={
        'placeholder':'数字のみ入力可能です。',
        'pattern':'^[0-9]+$'}))
    mail = forms.EmailField(
        label='メールアドレス',
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
        'placeholder':'sample@example.com',
        'pattern':'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'}))
    kinds = forms.ChoiceField(
        label='お問い合わせ内容',
        required=True,
        disabled=False,
        choices=[
            ('','選択してください'),
            ('仕事のご相談','仕事のご相談'),
            ('仕事のご依頼、お見積もり','仕事のご依頼、お見積もり'),
            ('サービスに関するお問い合わせ','サービスに関するお問い合わせ'),
            ('その他のお問い合わせ','その他のお問い合わせ')],
        widget=forms.Select,)
    message = forms.CharField(
        label='内容',
        required=False,
        max_length=255,
        widget=forms.Textarea,)

# 処理
def file_size(value):
    limit = 400*1000*1000
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
    header_select = forms.ChoiceField(
    label='ヘッダー指定',
    required=True,
    disabled=False,
    choices=[
        ('0','ヘッダーあり'),
        ('1','ヘッダーなし')],
    widget=forms.RadioSelect,)
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['csv']),
            file_size
            ]
    )
    num = forms.CharField(max_length=255)