from email import header
from tracemalloc import DomainFilter
from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import re
from django.conf import settings

####################################################
# ユーザー操作側
####################################################

# サインアップフォーム
class SignupForm(forms.Form):
    name = forms.CharField(
        label='ユーザーネーム',
        required=True,
        max_length=50,
    )
    email = forms.EmailField(
        label='メールアドレス',
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
        'placeholder':'sample@example.com',
        'pattern':'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'})
    )
    password1 = forms.CharField(
        label='パスワード',
        required=True,
        min_length=7,
        max_length=40,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='再確認',
        required=True,
        min_length=7,
        max_length=40,
        widget=forms.PasswordInput()
    )

# 二段階認証
class AuthForm(forms.Form):
    token = forms.CharField(
        label='5桁の番号',
        required=True,
        max_length=6,
    )

# ログインフォーム
class LoginForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
        'placeholder':'sample@example.com',
        'pattern':'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'})
    )
    password = forms.CharField(
        label='パスワード',
        required=True,
        max_length=40,
        widget=forms.PasswordInput()
    )

#お問い合わせ
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
        label='電話番号(数字のみ)',
        min_length=9,
        max_length=15,
        widget=forms.TextInput(attrs={
        # 'placeholder':'半角数字入力',
        'pattern':'^[0-9]+$'}))
    email = forms.EmailField(
        label='メールアドレス',
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
        # 'placeholder':'sample@example.com',
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

####################################################
# ここから処理側
####################################################

#最大容量
def file_size(value):
    LIMIT_SIZE = getattr(settings, 'LIMIT_SIZE', None)
    if value.size > LIMIT_SIZE:
        raise ValidationError(f'ファイルサイズが大きすぎます。{LIMIT_SIZE/1000/1000}MBより小さいサイズにしてください。')

#csv抽出
class CSVExtract(forms.Form):
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['csv']),
            file_size
            ])
    columuns = forms.CharField(max_length=255)
    code = forms.CharField(max_length=2000)

#csv分割
class CSVSplit(forms.Form):
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
            ])
    num = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
        # 'placeholder':'半角数字入力',
        'pattern':'^[0-9]+$'}))

#csv削除
class CSVRemove(forms.Form):
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['csv']),
            file_size
            ])
    columuns = forms.CharField(max_length=255)
    code = forms.CharField(max_length=2000)

#html_table変換
class ExcelTable(forms.Form):
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['xlsx']),
            file_size
            ])

#excel抽出
class ExcelExtract(forms.Form):
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['xlsx']),
            file_size
            ])
    columuns = forms.CharField(max_length=255)
    code = forms.CharField(max_length=2000)

#excel分割
class ExcelSplit(forms.Form):
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
            FileExtensionValidator(['xlsx']),
            file_size
            ])
    num = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
        # 'placeholder':'半角数字入力',
        'pattern':'^[0-9]+$'}))

#excel削除
class ExcelRemove(forms.Form):
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['xlsx']),
            file_size
            ])
    columuns = forms.CharField(max_length=255)
    code = forms.CharField(max_length=2000)

#image
class ImageResize(forms.Form):
    file = forms.FileField(
        validators=[
            FileExtensionValidator(['jpg','jpeg','png'])
        ]
    )
    resize_select = forms.ChoiceField(
    label='拡大・縮小',
    required=True,
    disabled=False,
    choices=[
        ('0','縮小'),
        ('1','拡大')],
    widget=forms.RadioSelect,)
    width = forms.CharField(max_length=10)
    height = forms.CharField(max_length=10)