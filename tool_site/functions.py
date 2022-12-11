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
from PIL import Image
import cv2


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
def CSV_extract_flow_one(file, code, columuns):
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
def CSV_extract_flow(file, code, columuns):
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
def CSV_split_flow(file, num, header_select):
    #csvファイル読み込み
    read_file = file.read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #csvファイルをdf形式に分割して変換
    files_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', header=header_select, dtype = 'object', chunksize=int(num))
    return files_data, enc

#csv行削除_単数ファイル
def CSV_remove_flow_one(file, code, columuns):
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

#csv行削除_複数ファイル
def CSV_remove_flow(file, code, columuns):
    #csvファイル読み込み
    read_file = file.read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #csvファイルをdf形式に変換
    file_data = pd.read_csv(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object')
    #データ処理
    df = file_data[~file_data[columuns].str.contains(code)]
    return df, enc

#zip化（全てutf-8で出力）
def CSV_to_zip(data,enc,header_select):
    #zipファイル準備
    response = HttpResponse(content_type='application/zip')
    with zipfile.ZipFile(response, 'w') as zf:
        #zipファイルに書き込み
        n = 1
        for i in data:
            #write版
            #zf.write(f'result-{n}.csv', i.to_csv(f'result-{n}.csv',encoding = enc, header=header_select, index= False))
            zf.writestr(f'result-{n}.csv', i.to_csv(encoding = enc, header=header_select, index= False))
            n += 1
    #Content-Dispositionでダウンロードの強制
    response['Content-Disposition'] = 'attachment; filename="results.zip"'
    return response

##html_table変換
def Excel_to_table_flow(file):

    #xlsxファイル読み込み
    df = pd.read_excel(file, dtype = 'object')
    df = df.replace(np.nan,'')

    #書き出し
    type_data = 'text/html; charset=' + 'utf-8'
    response = HttpResponse(content_type=type_data)
    response['Content-Disposition'] = 'attachment; filename="result.html"'
    df.to_html(response, index=False)
    return response

#excel行抽出_単数ファイル
def Excel_extract_flow_one(file, code, columuns):
    #excelファイルをdf形式に変換
    file_data = pd.read_excel(file[0], dtype = 'object')
    #データ処理
    df = file_data.loc[file_data[columuns].str.contains(code)]
    response = HttpResponse(content_type='application/vnd.ms-excel; charset="utf-8"')
    response['Content-Disposition'] = 'attachment; filename="result.xlsx"'
    df.to_excel(response,index=False)
    return response

#excel行抽出_複数ファイル
def Excel_extract_flow(file, code, columuns):
    #excelファイルをdf形式に変換
    file_data = pd.read_excel(file, dtype = 'object')
    #データ処理
    df = file_data.loc[file_data[columuns].str.contains(code)]
    return df

#excel行分割
def Excel_split_flow(file, num, header_select):
    #excelファイル読み込み
    read_file = file.read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #excelファイルをdf形式に分割して変換
    files_data = pd.read_excel(io.StringIO(read_file.decode(enc)), delimiter=',', header=header_select, dtype = 'object', chunksize=int(num))
    return files_data, enc

#zip化（全てutf-8で出力）
def Excel_to_zip(data,header_select):
    #zipファイル準備
    print(data)
    response = HttpResponse(content_type='application/zip; charset="utf-8"')
    with zipfile.ZipFile(response, mode='w') as zf:
        #zipファイルに書き込み
        n = 1
        for i in data:
            zf.write(f'result-{n}.xlsx', i.to_excel(f'result-{n}.xlsx', header=header_select, index= False))
            print(i)
            n += 1
    zf.close()
    #Content-Dispositionでダウンロードの強制
    response['Content-Disposition'] = 'attachment; filename="results.zip"'
    return response

#excel行削除_単数ファイル
def Excel_remove_flow_one(file, code, columuns):
    #excelファイル読み込み
    file_data = pd.read_excel(file[0], dtype = 'object')
    #データ処理
    df = file_data[~file_data[columuns].str.contains(code)]
    response = HttpResponse(content_type='application/vnd.ms-excel; charset="utf-8"')
    response['Content-Disposition'] = 'attachment; filename="result.xlsx"'
    df.to_excel(response,index=False)
    return response

#excel行削除_複数ファイル
def Excel_remove_flow(file, code, columuns):
    #excelファイル読み込み
    read_file = file.read()
    #文字コード識別
    enc = encode_cfm(read_file)
    #excelファイルをdf形式に変換
    file_data = pd.read_excel(io.StringIO(read_file.decode(enc)), delimiter=',', dtype = 'object')
    #データ処理
    df = file_data[~file_data[columuns].str.contains(code)]
    return df, enc

#image圧縮、縮小
def Image_resize_flow_one(file, resize_select, width, height):
    print('プリント')
    print(file)
    bfile =Image.open(file[0])
    img=np.asarray(np.array(bfile),  dtype=np.uint8)
    print('プリント')
    print(img)
    #img_array = np.asarray(bytearray(dfile.read()), dtype=np.uint8)
    img_resize = cv2.resize(img, width, height)
    print(img_resize)
    print('プリント')
    if resize_select == 0:
        img_resize = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)
    else:
        img_resize = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)

    response = HttpResponse(mimetype="image/png")
    img_resize.save(response, "PNG")
    return response