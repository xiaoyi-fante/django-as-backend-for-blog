from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseBadRequest
import simplejson
from .models import User
from django.db.models.query import QuerySet
from django.conf import settings
import jwt
import datetime
import bcrypt

AUTH_EXPIRE = 60*60*8

# def checkemail(request):
#     # 判断email
#     return HttpResponse()

def gen_token(user_id):
    return jwt.encode({
        'user_id':user_id,
        'timestamp': int(datetime.datetime.now().timestamp())
        },settings.SECRET_KEY, 'HS256').decode()


def reg(request:HttpRequest):
    # try:
    payload = simplejson.loads(request.body)
    email = payload['email']
    # 数据库中看看email有没有
    qs = User.objects.filter(email=email)
    print(qs) # 列表[]
    print(qs.query, '~~~~~~~~') # 查询机、结果集
    if qs: # 该email已经存在了
        print('1')
        return HttpResponseBadRequest()

    name = payload['name']
    password1 = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())
    print('-----',password1)

    user = User()
    user.email = email
    user.name = name
    user.password = password1 # md5 会被反查，计算速度太快了，穷举太快。
    print('===',user.password)

    try:
        user.save()
        print('---',user.password)
        print('-' * 30)
        return JsonResponse({'token':gen_token(user.id)}) # 200
    except Exception as e:
        # print(2)
        raise
    # except Exception as e:
    #     # print(3)
    #     return HttpResponseBadRequest()

def login(request:HttpRequest):
    # try:
    payload = simplejson.loads(request.body)
    email = payload['email']
    password1 = payload['password']
    print(password1)
    # 验证邮箱是否存在，存在之后，看密码
    user = User.objects.filter(email=email).get()
    print(1,user.password)

    # pass1=bcrypt.hashpw('abc'.encode(), bcrypt.gensalt())
    # print(2,pass1)

    if not user: # 查无此人
        return HttpResponseBadRequest()
    if bcrypt.checkpw(password1.encode(), user.password.encode()):
    # if not bcrypt.checkpw(password.encode(), pass1):
        return HttpResponseBadRequest()

    return JsonResponse({
        'user':{
            'user_id':user.id,
            'name':user.name,
            'email':user.email
        }, 'token':gen_token(user.id)
    }) # 200

    # except Exception as e:
    #     print(3)
    #     return HttpResponseBadRequest()






def test():
    pass