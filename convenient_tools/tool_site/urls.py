from django.urls import path
from tool_site import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='top'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('tool_extract/', views.Tool_extractView.as_view(), name='tool_extract'),
    # path('csv_export/', views.csv_exportView.as_view(), name='csv_export'),
    # path('csv_import/', views.csv_importView.as_view()),
]