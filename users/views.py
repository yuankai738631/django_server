# from django.shortcuts import render, HttpResponse
import json
import jwt
from legemangagement_serve.settings import SECRET_KEY
from django.http import JsonResponse

from users import models


# Create your views here.
def logon(request):
    """
        用户注册接口
    """
    code = 0
    message = ''
    if request.method == 'POST':
        json_params = json.loads(request.body.decode())
        if json_params:
            account_name = json_params.get('account_name', '')
            password = json_params.get('password', '')
            name = json_params.get('name', '')
            email = json_params.get('email', '')
            if account_name and password and name and email:
                users_data_count = models.Users.objects.all().count()
                if users_data_count == 0:
                    users = models.Users.objects.create(
                        account=account_name,
                        passWord=password,
                        name=name,
                        eMail=email
                    )
                    users.save()
                    message = '注册成功'
                else:
                    users_account_item = models.Users.objects.filter(account=account_name).first()
                    users_email_item = models.Users.objects.filter(eMail=email).first()
                    if users_account_item or users_email_item:
                        code = -3
                        message = '用户已存在，请直接登录'
                    else:
                        users = models.Users.objects.create(
                            account=account_name,
                            passWord=password,
                            name=name,
                            eMail=email
                        )
                        users.save()
                        message = '注册成功'
            else:
                code = -3
                message = '参数填写不完整'
        else:
            code = -2
            message = '参数错误'
    else:
        code = -1
        message = '请使用POST请求'
    return JsonResponse({"code": code, "message": message})


def user_login(request):
    obj = json.loads(request.body.decode())
    username = obj.get('username', None)
    password = obj.get('password', None)

    if username is None and password is None:
        return JsonResponse({'code': 500, 'message': '请求参数错误'})
    userinfo = models.Users.objects.filter(account=username).first()
    if not userinfo or userinfo.passWord != password:
        return JsonResponse({'code': 500, 'message': '账号或密码错误'})
    token = jwt.encode({'username': username, 'email': userinfo.eMail}, SECRET_KEY, algorithm='HS256')

    return JsonResponse({'code': 200, 'message': '登录成功', 'data': {'token': str(token), 'uid': userinfo.id}})
