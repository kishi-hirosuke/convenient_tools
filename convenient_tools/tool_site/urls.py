from django.urls import path
from tool_site import views


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('about/', views.AboutView.as_view()),
    path('tool_extract/', views.Tool_extractView.as_view()),
    # path('csv_export/', views.csv_exportView.as_view()),
    # path('csv_import/', views.csv_importView.as_view()),
]