from distutils.log import error
from tkinter import N
from urllib import response
import pandas as pd
import numpy as np
import csv, os, io
from django.http import HttpResponse
import chardet

'''エンコード識別関数（不使用）

def getEncode(file):
    encs = "cp932 shift_jis utf-8 utf-8-sig euc-jp iso-2022-jp".split()
    for enc in encs:
        try:
            pd.read_csv(io.StringIO(file.read().decode(enc)), delimiter=',')
        except UnicodeDecodeError:
            continue
        return enc

参考コード
def getEncode(filepath):
    encs = "iso-2022-jp euc-jp shift_jis utf-8".split()
    for enc in encs:
        with open(filepath, encoding=enc) as fr:
            try:
                fr = fr.read()
            except UnicodeDecodeError:
                continue
        return enc
'''

def csv_flow(file, code, columuns, flow):
    #エンコード識別、読み取り処理
    read_file = file.read()
    file_result = chardet.detect(read_file)
    enc = file_result['encoding']
    if enc == None:
        enc = 'cp932'
    file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',')
    #処理選択
    df = flow(file_data, code, columuns)
    #CSVカプセル化処理
    type_data = 'text/csv; charset=' + enc
    response = HttpResponse(content_type=type_data)
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    df.to_csv(path_or_buf = response, encoding = enc, index=False)
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