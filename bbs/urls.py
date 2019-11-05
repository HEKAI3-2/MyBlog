# coding=utf-8
"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog import views
# media
from django.views.static import serve
from django.conf import settings
from blog import urls as blog_urls
urlpatterns = [
    # 初始页
    url(r'^', views.index),
    
    url(r'^admin/', admin.site.urls),
    # 登录
    url(r'^login/', views.login),
    # 获取验证码
    url(r'^get_valid_img.png/', views.get_valid_img),
    # 注销
    url(r'^logout/', views.logout),
    # 注册
    url(r'^reg/', views.register),
    url(r'^index/', views.index),
    # 校验用户名是否已经存在的
    url(r'^check_username_exist/', views.check_username_exist),
    # media相关路由
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 去app中的urls.py写
    url(r'blog/', include(blog_urls)),

    url(r'^upload/', views.upload),

]
