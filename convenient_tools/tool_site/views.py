from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django import forms
from tool_site.forms import UploadForm
from tool_site.functions import process_file, to_csv_cp932, to_csv_utf_8
import csv, io
import pandas as pd

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

def Tool_extractView(request):
    if request.method == 'POST':
        upload = UploadForm(request.POST, request.FILES)
        if upload.is_valid():

            form_data = upload.cleaned_data
            word_data = form_data["word"]
            file = form_data["testfile"]
            print("プリント1")
            print(file)
            print("プリント1")
            try:
                file_data1 = pd.read_csv(io.StringIO(file.read().decode('cp932')), delimiter=',')
                print("プリント2")
                print(file_data1)
                print("プリント2")
                df = process_file(file_data1,word_data)
                response = to_csv_cp932(df)

            except UnicodeDecodeError:
                file_data2 = pd.read_csv(io.StringIO(file.read().decode('utf-8')), delimiter=',')
                print("プリント3")
                print(file_data2)
                print("プリント3")
                df = process_file(file_data2,word_data)
                response = to_csv_utf_8(df)
                #raise forms.ValidationError('拡張子がcsvのファイルをアップロードしてください')


            return response
    else:
        upload = UploadForm()
        return render(request, "tool_extract.html", {'form':upload})