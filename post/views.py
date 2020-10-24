from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpRequest,JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseNotFound
import simplejson
from user.views import authenticate
from post.models import Post,Content
import datetime
import math

@authenticate
def pub(request:HttpRequest):
    # try:
    print(request.body)
    payload = simplejson.loads(request.body)

    post = Post()
    post.title = payload['title']
    post.pubdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    post.author = request.user # 这里直接写request user的原因是，post表中的author字段我们将它定义为
                               # User表的外键，在post表中定义为author_id。
                               # 我们给它赋值为request.user，那么它会自动去匹配User表中的name字段，返回user的id给post表中author_id字段
    post.save() # 获得一个post id

    content = Content()
    content.post = post # 这里和上面的解释相同
    content.content = payload['content']

    return JsonResponse({
        'post_id':post.id
    })

    # except Exception as e:
    #     print(e)
    #     return HttpResponseBadRequest()



def get(request:HttpRequest, id):
    try:
        id = int(id)
        post = Post.objects.get(pk=id)
        print(post, '~~~~~~~~~~~~~')
        if post:
            return JsonResponse({
                'post':{
                    'post_id':post.id,
                    'title':post.title,
                    'author':post.author.name,
                    'author_id':post.author_id,
                    'postdate':post.postdate.timestamp(),
                    'content':post.content.content
                }
            })
        # get方法保证必须只有一条记录，否则抛异常
    except Exception as e:
        print(e)
        return HttpResponseNotFound()




def getall(request:HttpRequest):
    try: #页码
        page = int(request.GET.get('page',1))
        page = page if page > 0 else 1
    except:
        page = 1

    try: #页码行数
        #注意，这个数据不要轻易让浏览器端改变，如果允许改变，一定要控制范围
        size = int(request.GET.get('size', 20))
        size = size if size > 0 and size < 101 else 20
    except:
        size = 20

    try:
        # 按照id倒排
        start = (page - 1) * size
        posts = Post.objects.order_by('-id')[start:start+size]
        print(posts.query)
        return JsonResponse({
            'posts':[
                {
                    'post_id':post.id,
                    'title':post.title
                } for post in posts
            ]
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def validate(d:dict, name:str, type_func, default, validate_func):
    try: #页码
        result = type_func(d.get(name, default))
        result = validate_func(result, default)
    except:
        result = default
    return result

def getall(request:HttpRequest):
    #页码
    page = validate(request.GET, 'page', int, 1, lambda x,y:x if x > 0 else 1)
    size = validate(request.GET, 'size', int, 20, lambda x,y: x if x>0 and x<101 else y)

    try:
        #按照id倒排
        start = (page-1)*size
        posts = Post.objects.order_by('-id')

        print(posts.query)
        count = posts.count()

        posts = posts[start:start + size]
        print(posts.query)

        return JsonResponse({
            'posts':[
                {
                    'post_id':post.id,
                    'title':post.title
                } for post in posts
            ], 'pagination':{
                'page':page,
                'size':size,
                'count':count,
                'pages':math.ceil(count/size)
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

