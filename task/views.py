from django.shortcuts import render
import json
import datetime
from django.http import JsonResponse
from users import models
from task import models


# Create your views here.
def create_task(request):
    obj = json.loads(request.body.decode())
    task_name = obj('taskName', None)
    project_name = obj.get('projectName', None)
    uuid = obj.get('uuid', None)

    if task_name is None or project_name is None or uuid is None:
        return JsonResponse({'code': 500, 'message': '请求参数错误'})
    username = models.Users.objects.get(id=uuid).name
    create_time = str(datetime.datetime.now())
    task = models.Task.objects.create(
        taskName=task_name,
        projectName=project_name,
        status=0,
        creator=username,
        createTime=create_time
    )
    task.save()
    return JsonResponse({'code': 200, 'message': '创建成功'})
