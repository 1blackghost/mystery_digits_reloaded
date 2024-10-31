"""
URL configuration for mystery_digits_reloaded project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from main import views

urlpatterns = [
    path('get_csrf_token', views.get_csrf_token, name='get_csrf_token'),
    path('', views.index, name='index'),
    path("login",views.login,name="login"),
    path('getDetails', views.get_details, name='getDetails'),
    path('dashboard', views.dashboard, name='dashboard'),
    path("flush",views.flush,name="flush"),
    path("game",views.game,name="game"),
    path("ended",views.end,name="ended"),
    path("getL",views.get_leaderboard,name="getL"),
    path('resumeTime', views.resume_time, name='resume_time'),
    path('changesL', views.check_changes, name='check_changes'),


]