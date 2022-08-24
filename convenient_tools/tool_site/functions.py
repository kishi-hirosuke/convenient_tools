from distutils.log import error
from tkinter import N
from urllib import response
import pandas as pd
import numpy as np
import csv, os, io
from django.http import HttpResponse
import chardet
from charset_normalizer import detect
import time

def csv_flow(file, code, columuns, flow):
    #エンコード識別、読み取り処理
    start = time.time()
    read_file = file.read()
    elapsed_time = time.time() - start
    print (f"ラップ1:{elapsed_time}秒")
    file_result = detect(read_file)
    print(file_result)
    enc = file_result['encoding']

    if enc == 'shift-jis' or enc == 'SHIFT-JIS':
        pass
    elif enc == 'shift_jis' or enc == 'SHIFT_JIS':
        pass
    elif enc == 'utf-8' or enc == 'UTF-8':
        pass
    elif enc == 'utf_8' or enc == 'UTF_8':
        pass
    elif enc == 'utf-8-sig' or enc == 'UTF-8-SIG':
        pass
    elif enc == 'utf_8_sig' or enc == 'UTF_8_SIG':
        pass
    else:
        enc = 'cp932'

    print('エンコード:'+enc)
    elapsed_time = time.time() - start
    print (f"ラップ2:{elapsed_time}秒")
    file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object')
    elapsed_time = time.time() - start
    print (f"ラップ3:{elapsed_time}秒")
    #処理選択
    df = flow(file_data, code, columuns)
    elapsed_time = time.time() - start
    print (f"ラップ4:{elapsed_time}秒")
    #CSVカプセル化処理
    type_data = 'text/csv; charset=' + enc
    response = HttpResponse(content_type=type_data)
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    df.to_csv(path_or_buf = response, encoding = enc, index=False)
    elapsed_time = time.time() - start
    print (f"ラップ5:{elapsed_time}秒")
    return response

def flow_1(file_data, code, columuns):
    df_result = file_data.loc[file_data[columuns].str.contains(code)]
    return df_result

'''#csv書き出し関数
def to_csv(df,enc):
    type_data = 'text/csv; charset=' + enc
    response = HttpResponse(content_type=type_data)
    response['Content-Disposition'] = 'attachment; filename="result.csv"'

    df.to_csv(path_or_buf = response, encoding = enc, index=False)

    return response


#csv行抽出関数
def tool_extract_process(file,columuns,code):
    try:
        df_result = file.loc[file[columuns].str.contains(code)]
        return df_result
    except KeyError:
        raise print('存在しない列名が入力されています。')'''