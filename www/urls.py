"""www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

import views
import wx_views
from user import views as user_views
from logic import views as logic_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^ping$', views.ping),

    url(r'^wx$', wx_views.wx),
    url(r'^index$', logic_views.index),
    url(r'^job/get_job$', logic_views.get_job, name='get_job'),
    url(r'^job/post_job$', logic_views.post_job, name='post_job'),
]
