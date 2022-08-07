from tkinter import N
import pandas as pd
import numpy as np
import csv, os, io
from django.http import HttpResponse


#文字コードの自動判定関数
def getEncode(file):
    encs = "cp932 shift_jis utf-8 utf-8-sig euc-jp iso-2022-jp".split()
    for enc in encs:
        try:
            pd.read_csv(io.StringIO(file.read().decode(enc)), delimiter=',')
        except UnicodeDecodeError:
            continue
        return enc
'''
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

#csv編集テスト関数
def process_file(file_data,word_data):
    file = file_data
    word = word_data
    file[word] = 5

    df_result = file

    return df_result


#csv書き出し関数（おそらく文字コードの自動判定関数のenc使用したら1つにまとめれる）
def to_csv_cp932(df):
    response = HttpResponse(content_type='text/csv; charset=cp932')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    
    df.to_csv(path_or_buf = response, encoding = 'cp932', index=False)
    
    return response


#csv書き出し関数（おそらく文字コードの自動判定関数のenc使用したら1つにまとめれる）
def to_csv_utf_8(df):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    
    df.to_csv(path_or_buf = response, encoding = 'utf-8-sig', index=False)
    
    return response