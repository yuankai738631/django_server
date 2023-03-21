from django.urls import re_path as url
from .views import create_task

urlpatterns = [
    url('create_task', create_task)
]