from django.urls import path

# 先导入要添加路由的视图再配置路由
from accounts.views import *

urlpatterns = [
    path('register_api/', register),
    path('login_check/', login_check),
    path('pwd_miss_email_send/', pwd_miss_email_send),
    path('change_pwd_check/', change_pwd_check),
    path('create_temporary_user/', create_temporary_user),
]