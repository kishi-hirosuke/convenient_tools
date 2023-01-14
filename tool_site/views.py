import code
import email
import time
from ctypes import cdll
from dataclasses import dataclass, replace
from distutils.log import error
from tabnanny import check
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django import forms
from tool_site.models import AutoBizAccount, TimeUser
from django.contrib.auth.models import User
from tool_site.forms import  SignupForm, AuthForm, LoginForm, InquiryForm, CSVExtract, CSVSplit, CSVRemove, ExcelTable, ExcelExtract, ExcelSplit, ExcelRemove, ImageResize
from tool_site.functions import CSV_extract_flow, CSV_split_flow, CSV_remove_flow
from tool_site.functions import Excel_to_table_flow, Excel_extract_flow_one, Excel_extract_flow, Excel_split_flow, Excel_to_zip, Excel_remove_flow_one, Excel_remove_flow
from tool_site.functions import Image_resize_flow_one
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
import csv, io
import pandas as pd
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import datetime
from django.urls import reverse
from urllib.parse import urlencode

LIMIT_SIZE = getattr(settings, 'LIMIT_SIZE', None)/300/1000
LIMIT_SIZE = f'{LIMIT_SIZE}MB'

#topページ
class TopView(TemplateView):
    template_name = "index.html"

#aboutページ
class AboutView(TemplateView):
    template_name = "about.html"

############################################################
# ユーザー操作
############################################################

# サインアップ
def SignupView(request):
    if request.method == 'POST':
        time_user = SignupForm(request.POST)
        auth = AuthForm(request.POST)

        if time_user.is_valid():
            form_data = time_user.cleaned_data
            name, email = form_data['name'], form_data['email']  # name,email定義
            email_list = []  # メール送信時のemailリスト化
            email_list.append(email)

            if form_data['password1'] == form_data['password2']:  # password認証
                password = form_data['password1']  # password定義
            else:  # password不一致
                messages.info(request, f'パスワードが違います。')
                return redirect('signup')
            token = random.randint(100000,999999)  # token定義
            account_count = AutoBizAccount.objects.filter(email = email).count()  # 既存のuser確認

            if account_count >= 1:  # user件数が1件以上
                print('a')
                messages.info(request, f'既に登録されています。')
                return redirect('signup')

            else:  # user件数が0件
                subject = 'AutoBiz 二段階認証パスワード'
                body = f'氏名：{name}様\n\nこの度はAutoBizにご登録誠にありがとうございます。\n\n\n\n6桁の番号\n\n\n\n{token}\n\n\n\nこのE-mailは、発信者が意図した受信者による閲覧・利用を目的としたものです。万一、貴殿が意図された受信者でない場合には、直ちに送信者に連絡のうえ、このE-mailを破棄願います。'
                recipients = settings.EMAIL_HOST_USER

                try:  # メール送信処理
                    send_mail(subject, body, recipients, email_list)
                except BadHeaderError:  # ヘッダーエラー
                    messages.info(request, f'無効なヘッダーが見つかりました。')
                    return redirect('signup')
                except:  # メール送信時エラー
                    messages.info(request, f'メール処理の最中にエラーが発見されました。時間をおいて、再度試してください。')
                    return redirect('signup')

                TimeUser.objects.update_or_create(  # time_user登録or書き換え
                    email = email,
                    defaults={
                        'name':name,
                        'password':password,
                        'token':token,
                        'created_at':datetime.datetime.now()
                    }
                )
                context = {
                    'message':'ご登録のメールアドレス宛に6桁の番号を送信しました。フォームに入力してください。送信されていない場合は再度お試しください。',
                    'form1':time_user,
                    'form2':auth
                }
                return render(request, "User/signup.html", context)

        elif auth.is_valid():
            form_data = auth.cleaned_data
            token = form_data['token']
            auth_user_count = TimeUser.objects.filter(token = token).count()  # tokenの一致件数確認

            if auth_user_count == 1:  # tokenの一致が1件の場合
                auth_user = TimeUser.objects.get(token = token)  # time_userのデータ取得
                user = AutoBizAccount.objects.create_user(  # AutoBizAccount登録
                    name = auth_user.name,
                    password = auth_user.password,
                    email = auth_user.email,
                    created_at = datetime.datetime.now(),
                    updated_at = datetime.datetime.now()
                    )
                context = {
                    'message':f'{user.name}様のユーザー登録が完了しました。'
                }
                return render(request, 'User/success.html', context)
            elif auth_user_count == 0:  # tokenの一致が無し
                context = {
                    'message':'番号が違います。',
                    'form1':time_user,
                    'form2':auth
                }
                return render(request, 'User/signup.html', context)
            else:  # tokenの一致が2件以上
                context = {
                    'message':'メールアドレスが重複しているユーザーがいます。直ちに管理者にお問い合わせください。',
                    'form1':time_user,
                    'form2':auth
                }
                return render(request, 'User/signup.html', context)

        else:  # formバリデーション不足
            context = {
                'form1':time_user,
                'form2':auth
            }
            return render(request, "User/signup.html", context)

    else:
        time_user = SignupForm()
        auth = AuthForm
        context = {
            'form1':time_user,
            'form2':auth
        }
        return render(request, "User/signup.html", context)


# ログイン
def LoginView(request):

    if request.method == 'POST':
        user = LoginForm(request.POST)

        if user.is_valid():
            form_data = user.cleaned_data
            email = form_data['email']
            password = form_data['password']
            account = authenticate(username = email, password = password)  # アカウント認証

            if account is not None:  # accountありの場合
                login(request, account)
                return HttpResponseRedirect(reverse('top'))
            else:  # accountなしの場合
                messages.info(request, f'メールアドレス、またはパスワードが違います。')
                return redirect('signup')

    else:
        user = LoginForm()
        context = {
            'form':user
        }
        return render(request, 'User/login.html', context)


# ログアウト
@login_required
def LogoutView(request):
    logout(request)
    return redirect('login')


# お問い合わせ
@login_required
def InquiryView(request):
    if request.method == 'POST':
        inquiry = InquiryForm(request.POST)
        if inquiry.is_valid():
            form_data = inquiry.cleaned_data

            name, name_detail, company ,tel , email, kinds,  message = form_data['name'], form_data['name_detail'], form_data['company'], form_data['tel'], form_data['email'], form_data['kinds'], form_data['message']
            body = f'氏名：{name}\n\nふりがな：{name_detail}\n\n会社名：{company}\n\n電話番号：{tel}\n\n本文\n{message}'
            recipients = [settings.EMAIL_HOST_USER]
            try:
                send_mail(kinds, body, email, recipients)
            except BadHeaderError:
                return HttpResponse('無効なヘッダーが見つかりました。')
            return render(request, "inquiry.html", {'form':inquiry})
        else:
            return render(request, "inquiry.html", {'form':inquiry})
    else:
        inquiry = InquiryForm()
        return render(request, "inquiry.html", {'form':inquiry})


############################################################
# ここから処理
############################################################
@login_required
def Tool_CSV_categoryView(request):
    return render(request, "Category/CSV_category.html")
@login_required
def Tool_Excel_categoryView(request):
    return render(request, "Category/Excel_category.html")
@login_required
def Tool_Image_categoryView(request):
    return render(request, "Category/Image_category.html")


#csv行抽出
@login_required
def Tool_CSV_extractView(request):
    if request.method == 'POST':

        upload = CSVExtract(request.POST, request.FILES)

        if upload.is_valid():
            start = time.time()
            print('プリント')
            print(start)
            print('プリント')
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            try:
                response = CSV_extract_flow(file, code, columuns)
                print('プリント')
                print(time.time()-start)
                print('プリント')
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "CSV_flow/tool_CSV_extract.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "CSV_flow/tool_CSV_extract.html", context)

        else:
            return render(request, "CSV_flow/tool_CSV_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = CSVExtract()
        return render(request, "CSV_flow/tool_CSV_extract.html", {'form':upload,'limit_size':LIMIT_SIZE})


#csv分割
@login_required
def Tool_CSV_splitView(request):
    if request.method == 'POST':

        upload = CSVSplit(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            header_select, file, num = form_data["header_select"], form_data["file"], form_data["num"]
            try:
                response = CSV_split_flow(file, num, header_select[0])
                return response
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "CSV_flow/tool_CSV_split.html", context)

        else:
            return render(request, "CSV_flow/tool_CSV_split.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = CSVSplit()
        return render(request, "CSV_flow/tool_CSV_split.html", {'form':upload,'limit_size':LIMIT_SIZE})


#csv行削除
@login_required
def Tool_CSV_removeView(request):
    if request.method == 'POST':

        upload = CSVRemove(request.POST, request.FILES)

        if upload.is_valid():
            form_data = upload.cleaned_data
            file, code, columuns = request.FILES.getlist('file'), form_data["code"], form_data["columuns"]

            try:
                response = CSV_remove_flow(file, code, columuns)
                return response
            except KeyError:
                context = {
                    'error_message':'存在しない列名が入力されています。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "CSV_flow/tool_CSV_remove.html", context)
            except:
                context = {
                    'error_message':'無効なデータです。',
                    'form':upload,
                    'limit_size':LIMIT_SIZE,
                }
                return render(request, "CSV_flow/tool_CSV_remove.html", context)

        else:
            return render(request, "CSV_flow/tool_CSV_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})

    else:
        upload = CSVRemove()
        return render(request, "CSV_flow/tool_CSV_remove.html", {'form':upload,'limit_size':LIMIT_SIZE})


#html_table変換
@login_required
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
@login_required
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
@login_required
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
@login_required
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


# imageリサイズ
@login_required
def Tool_Image_resizeView(request):
    if request.method == 'POST':
        upload = ImageResize(request.POST, request.FILES)
        if upload.is_valid():
            form_data = upload.cleaned_data
            file, resize_select, width, height = request.FILES.getlist('file'), form_data["resize_select"], form_data["width"], form_data["height"]
            print(file)
            #try:
            if len(file) == 1:
                response = Image_resize_flow_one(file[0], resize_select, width, height)
                return response
            else:
                return render(request, "Image_flow/tool_image_resize.html")
    else:
        upload = ImageResize()
        return render(request, "Image_flow/tool_image_resize.html", {'form':upload,'limit_size':LIMIT_SIZE})

