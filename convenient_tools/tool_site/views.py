from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class Tool_extractView(TemplateView):
    template_name = "tool_extract.html"