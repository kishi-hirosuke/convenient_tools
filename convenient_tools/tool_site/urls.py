from django.urls import path
from .views import IndexView, AboutView, Tool_extractView

urlpatterns = [
    path('', IndexView.as_view()),
    path('about/', AboutView.as_view()),
    path('tool_extract/', Tool_extractView.as_view()),
]