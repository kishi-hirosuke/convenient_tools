from django import forms

class UploadForm(forms.Form):
    testfile = forms.FileField()
    word = forms.CharField()