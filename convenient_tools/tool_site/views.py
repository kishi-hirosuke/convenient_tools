import code
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django import forms
from tool_site.forms import UploadForm
from tool_site.functions import tool_extract_process, to_csv
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
            file = form_data["testfile"]
            code = form_data["code"]
            columuns = form_data["columuns"]

            #文字コード識別
            read_file = file.read()
            result = chardet.detect(read_file)
            enc = result['encoding']

            if enc == None:
                enc = 'cp932'

            #読み込み、編集
            file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',')
            df = tool_extract_process(file_data,columuns,code)
            response = to_csv(df,enc)
            return response

        else:
            return render(request, "tool_extract.html", {'form':upload})

    else:
        upload = UploadForm()
        return render(request, "tool_extract.html", {'form':upload})