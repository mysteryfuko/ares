from django.urls import path
from django.urls import include, path,re_path
from . import views,manage,api
from django.conf import settings

manage_patterns = [
    re_path(r'^$|index', manage.index, name='index'),
    path('login/', manage.login),
    path('edit/<str:act>/',manage.edit),
] 

urlpatterns = [
    path('', views.index),
    path('ajax/<str:action>/',api.ajax),
    path('api/<str:act>/',api.index),
    path('wxapi/<str:action>/',api.wxapi),
    path('PlayerDetail/<str:name>/',views.PlayerDetail),
    path('kill/<str:act>/<int:bossid>/',views.kill),
    path('manage/',include(manage_patterns)), 
    path('down_dkp/',views.down_dkp),
    path('do_loot/',manage.do_loot),
]

""" 
    
    
    
    path('down_epgp/',views.down_epgp),
    
    """