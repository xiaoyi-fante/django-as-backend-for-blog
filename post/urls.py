from django.conf.urls import url
from .views import pub, get, getall

urlpatterns = [
    url(r'^pub$', pub),
    url(r'^(\d+)$', get), # /(\d+) /post/10
    url(r'^$', getall),
]