"""
URL configuration for Dynamic_Pricing_Prediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from CSD import settings
from . import views as mainView
from Admins import views as admins
from Users import views as usr
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainView.Base, name="base"),
    path('Home/',mainView.Home,name="Home"),
    path('UserLogin/',mainView.UserLogin,name="UserLogin"),
    path('AdminLogin/',mainView.AdminLogin,name="AdminLogin"),
    path('UserRegister/',mainView.UserRegister,name="UserRegister"),

    # Admin views
    path("AdminHome/", admins.AdminHome, name="AdminHome"),
    path("AdminLoginCheck/", admins.AdminLoginCheck, name="AdminLoginCheck"),
    path('UserDetails/', admins.UserDetails, name='UserDetails'),
    path('ActivaUsers/', admins.ActivaUsers, name='ActivaUsers'),
  

    # User Views

    path("UserRegisterActions/", usr.UserRegisterActions, name="UserRegisterActions"),
    path("UserLoginCheck/", usr.UserLoginCheck, name="UserLoginCheck"),
    path("UserHome/", usr.UserHome, name="UserHome"),
    path('upload_video/', usr.upload_video, name='upload_video'),
    path('process_video/', usr.upload_video, name='process_video'),
    path('live_camera/', usr.live_camera, name='live_camera'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
