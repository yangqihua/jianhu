#coding=utf8
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

from user import views as user_views

urlpatterns = [
               url(r'^me$', user_views.me,name="me"),
               url(r'^recommand_list$', user_views.recommand_list, name="recommand_list$"),
               url(r'^collection_list$', user_views.collection_list, name="collection_list"),
               url(r'^fabu_list$', user_views.fabu_list, name="fabu_list"),
               url(r'^yinping_list$', user_views.yinping_list, name="yinping_list"),

               url(r'^recommand_detail$', user_views.recommand_detail, name="recommand_detail"),
               url(r'^collection_detail$', user_views.collection_detail, name="collection_detail"),
               url(r'^fabu_detail$', user_views.fabu_detail, name="fabu_detail"),
               url(r'^yingpin_detail$', user_views.yingpin_detail, name="yingpin_detail"),

               url(r'^edit_userinfo$', user_views.edit_userinfo, name="edit_userinfo"),
               url(r'^post_userinfo$', user_views.post_userinfo, name="post_userinfo"),
               ]
