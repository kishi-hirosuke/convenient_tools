import pandas as pd
import numpy as np
import csv,os
from django.http import HttpResponse

def process_file(data):
    test = data
    test['D'] = 0

    df_result = test

    return df_result

def to_csv(df):
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    
    df.to_csv(path_or_buf = response, encoding = 'utf-8-sig', index=False)
    
    return response