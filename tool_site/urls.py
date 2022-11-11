from django.urls import path
from tool_site import views


urlpatterns = [
    # 概要・お問い合わせ
    path('', views.IndexView.as_view(), name='top'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('inquiry/', views.inquiryView, name='inquiry' ),
    # csv処理
    path('tool_CSV_extract/', views.Tool_CSV_extractView, name='tool_extract'),
    path('tool_CSV_split/', views.Tool_CSV_splitView, name='tool_split'),
    path('tool_CSV_remove/', views.Tool_CSV_removeView, name='tool_remove'),
    # excel処理
    path('tool_Excel_table/', views.Tool_Excel_tableView, name='tool_table'),
    path('tool_Excel_extract/', views.Tool_Excel_extractView, name='excel_extract'),
    path('tool_Excel_split/', views.Tool_Excel_splitView, name='excel_split'),
    path('tool_Excel_remove/', views.Tool_Excel_removeView, name='excel_remove'),
]