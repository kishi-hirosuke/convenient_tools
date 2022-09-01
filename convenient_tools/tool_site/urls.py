from django.urls import path
from tool_site import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='top'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('tool_extract/', views.Tool_extractView, name='tool_extract'),
    path('tool_split/', views.Tool_splitView, name='tool_split'),
]