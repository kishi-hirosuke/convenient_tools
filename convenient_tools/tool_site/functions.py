from distutils.log import error
import re
from tkinter import N
from urllib import response
import pandas as pd
import numpy as np
import csv, os, io
import zipfile
from django.http import HttpResponse
from charset_normalizer import detect
import time


#文字コード識別
def encode_cfm(read_file):
    file_result = detect(read_file)
    enc = file_result['encoding']
    #例外エンコード処理
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
    return enc

#csv行抽出_単数ファイル
def extract_flow_one(file, code, columuns):
    #csvファイル読み込み
    read_file = file[0].read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #csvファイルをdf形式に変換
    file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object')
    #データ処理
    df = file_data.loc[file_data[columuns].str.contains(code)]
    type_data = 'text/csv; charset=' + enc
    response = HttpResponse(content_type=type_data)
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    df.to_csv(path_or_buf = response, encoding = enc, index=False)
    return response

#csv行抽出_複数ファイル
def extract_flow(file, code, columuns):
    #csvファイル読み込み
    read_file = file.read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #csvファイルをdf形式に変換
    file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object')
    #データ処理
    df = file_data.loc[file_data[columuns].str.contains(code)]
    return df, enc

#csv行分割
def split_flow(file, num, header_select):
    #csvファイル読み込み
    read_file = file.read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #csvファイルをdf形式に分割して変換
    files_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', header=header_select, dtype = 'object', chunksize=int(num))
    return files_data, enc

#zip化
def to_zip(data,enc,header_select):
    #zipファイル準備
    response = HttpResponse(content_type='application/zip')
    with zipfile.ZipFile(response, 'w') as zf:
        #zipファイルに書き込み
        n = 1
        for i in data:
            zf.writestr(f'result-{n}.csv', i.to_csv(encoding = enc, header=header_select, index= False))
            n += 1
    #Content-Dispositionでダウンロードの強制
    response['Content-Disposition'] = 'attachment; filename="results.zip"'
    return response

##html_table変換
def to_table_flow(file):

    #xlsxファイル読み込み
    df = pd.read_excel(file, dtype = 'object')
    df = df.replace(np.nan,'')

    #書き出し
    type_data = 'text/html; charset=' + 'utf-8'
    response = HttpResponse(content_type=type_data)
    response['Content-Disposition'] = 'attachment; filename="result.html"'
    df.to_html(response, index=False)
    return response

#csv行削除_単数ファイル
def remove_flow_one(file, code, columuns):
    #csvファイル読み込み
    read_file = file[0].read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #csvファイルをdf形式に変換
    file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object')
    #データ処理
    df = file_data[~file_data[columuns].str.contains(code)]
    type_data = 'text/csv; charset=' + enc
    response = HttpResponse(content_type=type_data)
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    df.to_csv(path_or_buf = response, encoding = enc, index=False)
    return response

#csv行抽出_複数ファイル
def remove_flow(file, code, columuns):
    #csvファイル読み込み
    read_file = file.read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #csvファイルをdf形式に変換
    file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object')
    #データ処理
    df = file_data[~file_data[columuns].str.contains(code)]
    return df, enc
