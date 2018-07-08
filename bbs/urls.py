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
from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.views.static import serve
from django.conf import settings
from blog import urls as blog_urls
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/',views.login),
    url(r'^v_code/',views.v_code),
    url(r'^index/',views.index),
    url(r'^register/',views.register),
    url(r'^logout/',views.logout),

    url(r'^media/(?P<path>.*)$',serve,{"document_root":settings.MEDIA_ROOT}), # 用户上传文件路由


    url(r'^blog/',include(blog_urls)), # 二级路由
    url(r'^updown/',views.updown),
    url(r'^comment_commit/',views.comment_commit),

    # 以上均匹配不上时，默认跳转至博客首页
    url(r'^$',views.index)





]

# django 调试工具路由
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'__debug__/',include(debug_toolbar.urls)),
    ] + urlpatterns
