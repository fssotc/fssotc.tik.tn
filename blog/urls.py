from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'(?P<pk>[0-9]+)/?$', views.PostDetail.as_view(), name="post"),
    url(r'$', views.posts_list, name="posts"),
]
