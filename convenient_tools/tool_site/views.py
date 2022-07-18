from django.http import HttpResponse
from django.views.generic import TemplateView, View
import csv, io

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class Tool_extractView(TemplateView):
    template_name = "tool_extract.html"

# class csv_exportView(View):

#     def post(self, request):
#         if 'csv' in request.FILES:
#             data = io.TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
#             csv_content = csv.reader(data)
#             return csv_content

#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment;  filename="item.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['1', 'い'])
#         writer.writerow(['2', 'ろ'])
#         writer.writerow(['3', 'は'])
#         return response


