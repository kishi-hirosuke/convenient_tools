import code
from ctypes import cdll
from distutils.log import error
from tabnanny import check
from urllib import response
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django import forms
from tool_site.forms import UploadForm
from tool_site.functions import csv_flow, flow_1
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
            file, code, columuns = form_data["testfile"], form_data["code"], form_data["columuns"]

            try:
                response = csv_flow(file, code, columuns, flow = flow_1)
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload
                }
                return render(request, "tool_extract.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload
                }
                return render(request, "tool_extract.html", context)

            '''#文字コード識別
            read_file = file.read()
            result = chardet.detect(read_file)
            enc = result['encoding']

            if enc == None:
                enc = 'cp932'

            #読み込み、編集
            file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',')
            try:
                df = tool_extract_process(file_data,columuns,code)
            except:
                error_message = 'error'
                context = {
                    'form':upload,
                    'eee': error_message
                }
                return render(request, "tool_extract.html", context)
            response = to_csv(df,enc)

            return response'''

        else:
            return render(request, "tool_extract.html", {'form':upload})

    else:
        upload = UploadForm()
        return render(request, "tool_extract.html", {'form':upload})