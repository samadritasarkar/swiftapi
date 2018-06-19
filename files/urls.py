"""swift URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from . import views
from django.conf.urls import url, include
from django.http import HttpResponseRedirect
app_name = 'files'
"""
   path('getcont/<container>/<token>', views.get_cont, name="getcont"),
   path('getobj/<container>/<object>/<token>', views.get_obj, name="getobj"),
   path('getdetail/', views.search_object, name="getdetail"), 
   path('getacc/', views.get_acc, name="getacc"),
   """
urlpatterns = [

    url('info/$', views.ContainerList.as_view(), name="acc_info"),
    url('info/(?P<container>[a-zA-Z0-9-]+)/$', views.ObjectList.as_view(), name="cont_info"),
    url('info/(?P<container>[a-zA-Z0-9-]+)/(?P<object>[a-zA-Z0-9.-_]+)/', views.download_object, name="obj_info")
]
