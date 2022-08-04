import pandas as pd
import numpy as np
import csv,os
from django.http import HttpResponse

def process_file(file_data,word_data):
    file = file_data
    word = word_data
    file[word] = 5

    df_result = file

    return df_result

def to_csv(df):
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    
    df.to_csv(path_or_buf = response, encoding = 'utf-8-sig', index=False)
    
    return response