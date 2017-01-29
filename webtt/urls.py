"""webtt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles import views
import django.contrib.auth.views
from django.conf.urls.static import  static

from video import home, preparation

urlpatterns = [
    url(r'^$', home.index, name='home'),
    url(r'^preparation/$', preparation.index, name='preparation'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', django.contrib.auth.views.login, name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/login'}),
    url(r'^video/', include('video.urls')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]
