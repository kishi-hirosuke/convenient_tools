import code
import email
import time
from ctypes import cdll
from dataclasses import dataclass, replace
from distutils.log import error
from tabnanny import check
from urllib import response
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django import forms
from tool_site.forms import UploadExtract, UploadSplit, InquiryForm
from tool_site.functions import extract_flow, split_flow
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
import csv, io
import pandas as pd


class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

# お問い合わせ
def inquiryView(request):
    if request.method == 'POST':
        inquiry = InquiryForm(request.POST)
        if inquiry.is_valid():
            form_data = inquiry.cleaned_data

            name, name_detail, company ,tel , mail, kinds,  message = form_data['name'], form_data['name_detail'], form_data['company'], form_data['tel'], form_data['mail'], form_data['kinds'], form_data['message']
            body = f'氏名：{name}\n\nふりがな：{name_detail}\n\n会社名：{company}\n\n電話番号：{tel}\n\n本文\n{message}'
            recipients = [settings.EMAIL_HOST_USER]
            try:
                send_mail(kinds, body, mail, recipients)
            except BadHeaderError:
                return HttpResponse('無効なヘッダーが見つかりました。')
            return render(request, "inquiry.html", {'form':inquiry})
    else:
        inquiry = InquiryForm()
        return render(request, "inquiry.html", {'form':inquiry})

# 処理
def Tool_extractView(request):
    if request.method == 'POST':

        upload = UploadExtract(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = form_data["file"], form_data["code"], form_data["columuns"]

            try:
                start = time.time()
                response = extract_flow(file, code, columuns)
                elapsed_time = time.time() - start
                print (f"処理時間:{elapsed_time}秒")
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
        upload = UploadExtract()
        return render(request, "tool_extract.html", {'form':upload})



def Tool_splitView(request):
    if request.method == 'POST':

        upload = UploadSplit(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, num = form_data["file"], form_data["num"]

            start = time.time()
            response = split_flow(file, num)
            elapsed_time = time.time() - start
            print (f"処理時間:{elapsed_time}秒")
            return response

            # try:
            #     start = time.time()
            #     response = split_flow(file, num)
            #     elapsed_time = time.time() - start
            #     print (f"処理時間:{elapsed_time}秒")
            #     return response
            # except:
            #     context = {
            #         'error_message':'無効なデータです。',
            #         'form':upload
            #     }
            #     return render(request, "tool_split.html", context)

        else:
            return render(request, "tool_split.html", {'form':upload})

    else:
        upload = UploadSplit()
        return render(request, "tool_split.html", {'form':upload})