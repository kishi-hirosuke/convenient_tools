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

def extract_flow(file, code, columuns):
    #エンコード識別、読み取り処理
    start = time.time()
    #csvファイル読み込み
    read_file = file.read()
    #エンコード識別
    enc = encode_cfm(read_file)
    elapsed_time = time.time() - start
    print (f"ラップ1:{elapsed_time}秒")
    #csvファイルをdf形式に変換
    file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object')
    elapsed_time = time.time() - start
    print (f"ラップ2:{elapsed_time}秒")
    #データ処理
    df = file_data.loc[file_data[columuns].str.contains(code)]
    elapsed_time = time.time() - start
    print (f"ラップ3:{elapsed_time}秒")
    #書き出し
    type_data = 'text/csv; charset=' + enc
    response = HttpResponse(content_type=type_data)
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    df.to_csv(path_or_buf = response, encoding = enc, index=False)
    elapsed_time = time.time() - start
    print (f"ラップ4:{elapsed_time}秒")
    return response

def split_flow(file, num):
    start = time.time()
    #csvファイル読み込み
    read_file = file.read()
    #エンコード識別
    enc = encode_cfm(read_file)
    elapsed_time = time.time() - start
    print (f"ラップ1:{elapsed_time}秒")
    #csvファイルをdf形式に分割して変換
    files = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object', chunksize=int(num))
    elapsed_time = time.time() - start
    print (f"ラップ2:{elapsed_time}秒")
    #zipファイル準備
    response = HttpResponse(content_type='application/zip')
    with zipfile.ZipFile(response, 'w') as zf:
        #zipファイルに書き込み
        n = 1
        for file in files:
            zf.writestr(f'result-{n}.csv', file.to_csv(encoding = enc, index= False))
            n += 1
    #Content-Dispositionでダウンロードの強制
    response['Content-Disposition'] = 'attachment; filename="results.zip"'
    elapsed_time = time.time() - start
    print (f"ラップ3:{elapsed_time}秒")
    return response