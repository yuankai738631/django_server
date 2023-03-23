import json
import datetime
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    username = Users.objects.filter(id=uuid).first()
    if not username:
        return JsonResponse({'code': 500, 'message': '用户信息异常'})
    task = Task.objects.filter(taskName=task_name).first()
    if task is not None:
        return JsonResponse({'code': 500, 'message': '任务名称已使用'})
    create_time = str(datetime.datetime.now())
    task = Task.objects.create(
        taskName=task_name,
        projectName=project_name,
        status=0,
        creator=username.name,
        createTime=create_time
    )
    task.save()
    return JsonResponse({'code': 200, 'message': '创建成功'})


def remove_task(request):
    obj = json.loads(request.body.decode())
    task_id = obj.get('id', None)

    if task_id is None:
        return JsonResponse({'code': 500, 'message': '请求参数错误'})
    Task.objects.filter(id=task_id).delete()
    return JsonResponse({'code': 200, 'message': '删除成功'})


def query_tasks(request):
    obj = json.loads(request.body.decode())
    task_name = obj.get('taskName', None)
    project_name = obj.get('projectName', None)
    status = obj.get('taskStatus', None)
    page = obj.get('page', 1)
    page_size = obj.get('pageSize', 10)

    current_page = page
    project_list = []
    if task_name is None and project_name is None and status is None:
        task_list = Task.objects.all().order_by('-createTime')
    elif task_name and project_name and status:
        task_list = Task.objects.filter(Q(taskName__icontains=task_name), Q(projectName=project_name), Q(status=status))
    else:
        if task_name and project_name is None and status is None:
            task_list = Task.objects.filter(Q(taskName__icontains=task_name)).order_by('-createTime')
        elif task_name and project_name and status is None:
            task_list = Task.objects.filter(Q(taskName__icontains=task_name), Q(projectName=project_name)).order_by('-createTime')
        elif task_name and project_name is None and status is not None:
            task_list = Task.objects.filter(Q(taskName__icontains=task_name), Q(status=status)).order_by('-createTime')
        elif task_name is None and project_name and status is None:
            task_list = Task.objects.filter(Q(projectName=project_name)).order_by('-createTime')
        elif task_name is None and project_name and status is not None:
            task_list = Task.objects.filter(Q(projectName=project_name), Q(status=status)).order_by('-createTime')
        elif task_name is None and project_name is None and status is not None:
            task_list = Task.objects.filter(Q(status=status)).order_by('-createTime')
    default_data = []
    for task in task_list:
        project_list.append(task.projectName)
        default_data.append({
            "creator": task.creator,
            "createTime": task.createTime,
            "id": task.id,
            "projectName": task.projectName,
            "status": task.status,
            "taskName": task.taskName,
        })
    paginator = Paginator(default_data, page_size)
    total = paginator.count
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
        current_page = 1
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
        current_page = paginator.num_pages
    # json_list = json.loads(serializers.serialize('json', tasks))
    data = tasks.object_list
    return JsonResponse({
        'code': 200,
        'message': '查询成功',
        'data': {'list': data, 'total': total, 'currentPage': current_page, 'projectList': project_list}
    })
