"""talkhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from blogapp import views

urlpatterns = [
    url(r'(?P<id>\d+)/post_edit/$', views.post_edit, name='post_edit'),
    url(r'(?P<id>\d+)/post_delete/$', views.post_delete, name='post_delete'),
    url(r'(?P<id>\d+)/(?P<key>[a-zA-Z0-9_]+)/$', views.chat_page, name='chat_page'),
    url(r'post_create/$', views.post_create, name='post_create'),
    url(r'refresh/(?P<id>\d+)/$', views.comment_refresh, name='comment_refresh'),
    url(r'(?P<id>\d+)/(?P<key>[a-zA-Z0-9_]+)/recommend/$', views.post_recommend, name='post_recommend'),
    url(r'comment-delete/(?P<id>\d+)/(?P<comid>\d+)/$', views.comment_delete, name='comment_delete'),
]
