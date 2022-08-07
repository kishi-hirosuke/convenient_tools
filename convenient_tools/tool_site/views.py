from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django import forms
from tool_site.forms import UploadForm
from tool_site.functions import process_file, to_csv_cp932, to_csv_utf_8, getEncode
import csv, io
import pandas as pd
import chardet


class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

def Tool_extractView(request):
    if request.method == 'POST':
        upload = UploadForm(request.POST, request.FILES)
        if upload.is_valid():

            form_data = upload.cleaned_data
            word = form_data["word"]
            file = form_data["testfile"]

            #データ状況確認用ここから
            print('ファイル名')
            print(file)

            print('タイプ')
            print(type(file))

            enc = getEncode(file)
            print('エンコード')
            print(enc)

            print('タイプ')
            print(type(enc))
            #データ状況確認ここまで

            
            try:
                file_data1 = pd.read_csv(io.StringIO(file.read().decode('cp932')), delimiter=',')
                df = process_file(file_data1,word)
                response = to_csv_cp932(df)

            except UnicodeDecodeError:
                file_data2 = pd.read_csv(io.StringIO(file.read().decode('utf-8')), delimiter=',')
                df = process_file(file_data2,word)
                response = to_csv_utf_8(df)
                #raise forms.ValidationError('拡張子がcsvのファイルをアップロードしてください')


            return response
    else:
        upload = UploadForm()
        return render(request, "tool_extract.html", {'form':upload})