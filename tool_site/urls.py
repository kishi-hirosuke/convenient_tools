from django.urls import path
from tool_site import views


urlpatterns = [
    # 概要・お問い合わせ
    path('', views.IndexView.as_view(), name='top'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('inquiry/', views.inquiryView, name='inquiry' ),
    # csv処理
    path('tool_extract/', views.Tool_extractView, name='tool_extract'),
    path('tool_split/', views.Tool_splitView, name='tool_split'),
    path('tool_remove/', views.Tool_removeView, name='tool_remove'),
    # excel処理
    path('tool_table/', views.Tool_tableView, name='tool_table'),
    path('tool_extract/', views.Tool_extract_2_View, name='excel_extract'),
    path('tool_split/', views.Tool_split_2_View, name='excel_split'),
    path('tool_remove/', views.Tool_remove_2_View, name='excel_remove'),
]