"""atgBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
app_name = "blog"
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from . import views
urlpatterns = [
    path('',views.login,name= "login"),
    path('register/',views.register,name="register"),
    path('check_username', views.checkUsername,name="check_username"),
    path('blog/', views.blog, name= "blog"),
    re_path(r'private/(?P<article_id>[0-9]+)',views.privacy, name="privacy"),
    re_path(r'^user$', views.userView, name= "userView"),
    re_path(r'^user_detail/(?P<user_id>[0-9]+)$', views.userDetail,name= "userDetail"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('add/', views.add, name= "add"),
    re_path(r'^article/(?P<article_id>[0-9]+)/$',views.fullArticle,name="fullArticle")
]
