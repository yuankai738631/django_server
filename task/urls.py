from django.urls import re_path as url
from .views import create_task, query_tasks, remove_task

urlpatterns = [
    url('create_task', create_task),
    url('query_tasks', query_tasks),
    url('remove_task', remove_task)
]
