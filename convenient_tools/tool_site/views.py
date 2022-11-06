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
from tool_site.forms import UploadExtract, UploadSplit, InquiryForm, UploadTable, UploadRemove
from tool_site.functions import extract_flow, split_flow, to_zip, extract_flow_one, to_table_flow, remove_flow_one, remove_flow
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
import csv, io
import pandas as pd

LIMIT_SIZE = getattr(settings, 'LIMIT_SIZE', None)/1000/1000
LIMIT_SIZE = f'{LIMIT_SIZE}MB'

#topページ
class IndexView(TemplateView):
    template_name = "index.html"

#aboutページ
class AboutView(TemplateView):
    template_name = "about.html"

#お問い合わせ
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

#csv行抽出
def Tool_extractView(request):
    if request.method == 'POST':

        upload = UploadExtract(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            try:
                #ファイル数判定
                if len(file) == 1:
                    response = extract_flow_one(file, code, columuns)
                else:
                    data = []
                    for i in file:
                        file_data = extract_flow(i, code, columuns)
                        data.append(file_data[0])
                    response = to_zip(data,file_data[1],True)
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_extract.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_extract.html", context)

        else:
            return render(request, "tool_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = UploadExtract()
        return render(request, "tool_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

#csv分割
def Tool_splitView(request):
    if request.method == 'POST':

        upload = UploadSplit(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            header_select, file, num = form_data["header_select"], form_data["file"], form_data["num"]
            print(header_select)
            if header_select == '0':
                header_select = ['infer',True]
            else:
                header_select = [None,False]

            try:
                data = split_flow(file, num, header_select[0])
                response = to_zip(data[0],data[1],header_select[1])
                return response
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_split.html", context)

        else:
            return render(request, "tool_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = UploadSplit()
        return render(request, "tool_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

#csv行削除
def Tool_removeView(request):
    if request.method == 'POST':

        upload = UploadRemove(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            try:
                #ファイル数判定
                if len(file) == 1:
                    response = remove_flow_one(file, code, columuns)
                else:
                    data = []
                    for i in file:
                        file_data = remove_flow(i, code, columuns)
                        data.append(file_data[0])
                    response = to_zip(data,file_data[1],True)
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_remove.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_remove.html", context)

        else:
            return render(request, "tool_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = UploadRemove()
        return render(request, "tool_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})

#html_table変換
def Tool_tableView(request):
    if request.method == 'POST':

        upload = UploadTable(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file = form_data["file"]

            try:
                response = to_table_flow(file)
                return response
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_table.html", context)

        else:
            return render(request, "tool_table.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = UploadTable()
        return render(request, "excel_flow/tool_table.html", {'form':upload,'limit_size':LIMIT_SIZE})

#excel行抽出
def Tool_extractView(request):
    if request.method == 'POST':

        upload = UploadExtract(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            try:
                #ファイル数判定
                if len(file) == 1:
                    response = extract_flow_one(file, code, columuns)
                else:
                    data = []
                    for i in file:
                        file_data = extract_flow(i, code, columuns)
                        data.append(file_data[0])
                    response = to_zip(data,file_data[1],True)
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_extract.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_extract.html", context)

        else:
            return render(request, "tool_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = UploadExtract()
        return render(request, "tool_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

#excel分割
def Tool_splitView(request):
    if request.method == 'POST':

        upload = UploadSplit(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            header_select, file, num = form_data["header_select"], form_data["file"], form_data["num"]
            print(header_select)
            if header_select == '0':
                header_select = ['infer',True]
            else:
                header_select = [None,False]

            try:
                data = split_flow(file, num, header_select[0])
                response = to_zip(data[0],data[1],header_select[1])
                return response
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_split.html", context)

        else:
            return render(request, "tool_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = UploadSplit()
        return render(request, "tool_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

#excel行削除
def Tool_removeView(request):
    if request.method == 'POST':

        upload = UploadRemove(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            try:
                #ファイル数判定
                if len(file) == 1:
                    response = remove_flow_one(file, code, columuns)
                else:
                    data = []
                    for i in file:
                        file_data = remove_flow(i, code, columuns)
                        data.append(file_data[0])
                    response = to_zip(data,file_data[1],True)
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_remove.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_remove.html", context)

        else:
            return render(request, "tool_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = UploadRemove()
        return render(request, "tool_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})





