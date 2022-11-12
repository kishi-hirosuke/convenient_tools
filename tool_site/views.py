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
from tool_site.forms import InquiryForm, CSVExtract, CSVSplit, CSVRemove, ExcelTable, ExcelExtract, ExcelSplit, ExcelRemove
from tool_site.functions import  CSV_extract_flow_one, CSV_extract_flow, CSV_split_flow, CSV_to_zip, CSV_remove_flow_one, CSV_remove_flow
from tool_site.functions import Excel_to_table_flow, Excel_extract_flow_one, Excel_extract_flow, Excel_split_flow, Excel_to_zip, Excel_remove_flow_one, Excel_remove_flow
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
def Tool_CSV_extractView(request):
    if request.method == 'POST':

        upload = CSVExtract(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            #try:
                #ファイル数判定
            if len(file) == 1:
                response = CSV_extract_flow_one(file, code, columuns)
            else:
                data = []
                for i in file:
                    file_data = CSV_extract_flow(i, code, columuns)
                    data.append(file_data[0])
                response = CSV_to_zip(data,file_data[1],True)
            return response
            # except KeyError:
            #     context = {
            #         'error_message':'存在しない列名が入力されています。',
            #         'form':upload,
            #         'limit_size':LIMIT_SIZE,
            #     }
            #     return render(request, "tool_CSV_extract.html", context)
            # except:
            #     context = {
            #         'error_message':'無効なデータです。',
            #         'form':upload,
            #         'limit_size':LIMIT_SIZE,
            #     }
            #     return render(request, "tool_CSV_extract.html", context)

        else:
            return render(request, "tool_CSV_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = CSVExtract()
        return render(request, "tool_CSV_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

#csv分割
def Tool_CSV_splitView(request):
    if request.method == 'POST':

        upload = CSVSplit(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            header_select, file, num = form_data["header_select"], form_data["file"], form_data["num"]
            print(header_select)
            if header_select == '0':
                header_select = ['infer',True]
            else:
                header_select = [None,False]

            try:
                data = CSV_split_flow(file, num, header_select[0])
                response = CSV_to_zip(data[0],data[1],header_select[1])
                return response
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_CSV_split.html", context)

        else:
            return render(request, "tool_CSV_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = CSVSplit()
        return render(request, "tool_CSV_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

#csv行削除
def Tool_CSV_removeView(request):
    if request.method == 'POST':

        upload = CSVRemove(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            try:
                #ファイル数判定
                if len(file) == 1:
                    response = CSV_remove_flow_one(file, code, columuns)
                else:
                    data = []
                    for i in file:
                        file_data = CSV_remove_flow(i, code, columuns)
                        data.append(file_data[0])
                    response = CSV_to_zip(data,file_data[1],True)
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_CSV_remove.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "tool_CSV_remove.html", context)

        else:
            return render(request, "tool_CSV_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = CSVRemove()
        return render(request, "tool_CSV_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})

#html_table変換
def Tool_Excel_tableView(request):
    if request.method == 'POST':

        upload = ExcelTable(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file = form_data["file"]

            try:
                response = Excel_to_table_flow(file)
                return response
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "Excel_flow/tool_Excel_table.html", context)

        else:
            return render(request, "Excel_flow/tool_Excel_table.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = ExcelTable()
        return render(request, "Excel_flow/tool_Excel_table.html", {'form':upload,'limit_size':LIMIT_SIZE})

#excel行抽出
def Tool_Excel_extractView(request):
    if request.method == 'POST':

        upload = ExcelExtract(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            #try:
            #ファイル数判定
            if len(file) == 1:
                response = Excel_extract_flow_one(file, code, columuns)
            else:
                data = []
                for i in file:
                    file_data = Excel_extract_flow(i, code, columuns)
                    data.append(file_data)
                response = Excel_to_zip(data,True)
            return response
            # except KeyError:
            #     context = {
            #         'error_message':'存在しない列名が入力されています。',
            #         'form':upload,
            #         'limit_size':LIMIT_SIZE,
            #     }
            #     return render(request, "Excel_flow/tool_Excel_extract.html", context)
            # except:
            #     context = {
            #         'error_message':'無効なデータです。',
            #         'form':upload,
            #         'limit_size':LIMIT_SIZE,
            #     }
            #     return render(request, "Excel_flow/tool_Excel_extract.html", context)

        else:
            return render(request, "Excel_flow/tool_Excel_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = ExcelExtract()
        return render(request, "Excel_flow/tool_Excel_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

#excel分割
def Tool_Excel_splitView(request):
    if request.method == 'POST':

        upload = ExcelSplit(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            header_select, file, num = form_data["header_select"], form_data["file"], form_data["num"]
            print(header_select)
            if header_select == '0':
                header_select = ['infer',True]
            else:
                header_select = [None,False]

            try:
                data = Excel_split_flow(file, num, header_select[0])
                response = Excel_to_zip(data[0],data[1],header_select[1])
                return response
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "Excel_flow/tool_Excel_split.html", context)

        else:
            return render(request, "Excel_flow/tool_Excel_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = ExcelSplit()
        return render(request, "Excel_flow/tool_Excel_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

#excel行削除
def Tool_Excel_removeView(request):
    if request.method == 'POST':

        upload = ExcelRemove(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            try:
                #ファイル数判定
                if len(file) == 1:
                    response = Excel_remove_flow_one(file, code, columuns)
                else:
                    data = []
                    for i in file:
                        file_data = Excel_remove_flow(i, code, columuns)
                        data.append(file_data[0])
                    response = Excel_to_zip(data,file_data[1],True)
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "Excel_flow/tool_Excel_remove.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "Excel_flow/tool_Excel_remove.html", context)

        else:
            return render(request, "Excel_flow/tool_Excel_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = ExcelRemove()
        return render(request, "Excel_flow/tool_Excel_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})





