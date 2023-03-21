from django.shortcuts import render
import json
import datetime
from django.http import JsonResponse
from users.models import Users
from task.models import Task


# Create your views here.
def create_task(request):
    obj = json.loads(request.body.decode())
    task_name = obj.get('taskName', None)
    project_name = obj.get('projectName', None)
    uuid = obj.get('uuid', None)

    if task_name is None or project_name is None or uuid is None:
        return JsonResponse({'code': 500, 'message': '请求参数错误'})
    username = Users.objects.filter(id=uuid).first().name
    if not username:
        return JsonResponse({'code': 500, 'message': '用户信息异常'})
    create_time = str(datetime.datetime.now())
    task = Task.objects.create(
        taskName=task_name,
        projectName=project_name,
        status=0,
        creator=username,
        createTime=create_time
    )
    task.save()
    return JsonResponse({'code': 200, 'message': '创建成功'})


def query_tasks(request):
    obj = json.loads(request.body.decode())

    task_list = Task.objects.all()
    data = []
    for task_item in task_list:
        print(task_item)
        dic = {
            'id': task_item.id,
            'taskName': task_item.taskName,
            'projectName': task_item.projectName,
            'status': task_item.status,
            'creator': task_item.creator,
            'createTime': task_item.createTime
        }
        data.append(dic)
    return JsonResponse({'code': 200, 'message': '查询成功', 'data': {'list': data}})