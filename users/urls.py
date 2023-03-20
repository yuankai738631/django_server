from django.urls import re_path as url
from .views import logon, user_login

urlpatterns = [
    url('UserRegistration', logon),
    url('login', user_login)
]