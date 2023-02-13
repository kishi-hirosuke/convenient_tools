from django.urls import path
from tool_site import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #トップページ
    path('', views.TopView.as_view(), name='top'),
    #ツール一覧
    path('tools/', views.ToolsView.as_view(), name='tools'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('help/', views.HelpView.as_view(), name='help'),
    #stripe決済
    path('create_checkout_session/', views.create_checkout_session, name='checkout_session'),
    path('premium/', views.SubscriptionPremiumView.as_view(), name='premium'),
    path('success/', views.SubscriptionSuccessView.as_view(), name='success'),
    path('cancel/', views.SubscriptionCancelView.as_view(), name='cancel'),
    # サインアップ
    path('signup/', views.SignupView, name='signup'),
    # ログイン
    path('login/', views.LoginView, name='login'),
    # ログアウト
    path('logout/', views.LogoutView, name='logout'),
    # パスワード忘却処置
    path('lost_password/', views.Lost_PasswordView, name='lost_password'),
    # アカウント情報変更
    path('edit_account', views.Edit_AccountView, name='edit_account'),
    # お問い合わせ
    path('inquiry/', views.InquiryView, name='inquiry' ),
    # カテゴリ
    path('CSV_category/', views.Tool_CSV_categoryView.as_view(), name='csv_category'),
    path('Excel_category/', views.Tool_Excel_categoryView.as_view(), name='excel_category'),
    path('Image_category/', views.Tool_Image_categoryView.as_view(), name='image_category'),
    # csv処理
    path('tool_CSV_extract/', views.Tool_CSV_extractView, name='csv_extract'),
    path('tool_CSV_split/', views.Tool_CSV_splitView, name='csv_split'),
    path('tool_CSV_remove/', views.Tool_CSV_removeView, name='csv_remove'),
    # excel処理
    path('tool_Excel_table/', views.Tool_Excel_tableView, name='excel_table'),
    path('tool_Excel_extract/', views.Tool_Excel_extractView, name='excel_extract'),
    path('tool_Excel_split/', views.Tool_Excel_splitView, name='excel_split'),
    path('tool_Excel_remove/', views.Tool_Excel_removeView, name='excel_remove'),
    # image処理
    path('tool_Image_resize/', views.Tool_Image_resizeView, name='image_resize'),
]