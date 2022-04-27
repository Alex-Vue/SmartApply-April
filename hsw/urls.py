"""hsw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from users import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', views.index),
  path("sign-in/", views.signin_view),
  path("sign-up/", views.signup_view),
  path('log-out/', views.logout_view),
  path('home', views.home),
  path('user-profile', views.profile_view),
  path("cal", views.cal),
  path("important-files/", views.files, name="importantfiles"),
  path("process-of-applications", views.applications),
  path("resv_list/", views.ajax_resv_list),
  path("app-org", views.app_org),
  path("documents/<path:path>", views.download),
  path("important-files/delete/<path:document>", views.deleteFile),
  
  ###################################### 20220418
  path("resv_cnt/", views.ajax_resv_cnt),
  ###################################### 20220418
]
