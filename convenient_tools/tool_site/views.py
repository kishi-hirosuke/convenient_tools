from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from tool_site.forms import UploadForm
from tool_site.functions import process_file, to_csv
import csv, io
import pandas as pd

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

def Tool_extractView(request):
    if request.method == 'POST':
        upload = UploadForm(request.POST, request.FILES)
        if upload.is_valid():

            form_data = upload.cleaned_data
            word_data = form_data["word"]
            
            file_data = pd.read_csv(io.StringIO(request.FILES['testfile'].read().decode('utf-8')), delimiter=',')
            df = process_file(file_data,word_data)

            response = to_csv(df)

            return response
    else:
        upload = UploadForm()
        return render(request, "tool_extract.html", {'form':upload})