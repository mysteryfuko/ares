from django.urls import path
from django.urls import include, path,re_path
from . import views
from django.conf import settings

""" manage_patterns = [
    re_path(r'^$|index', manage.index, name='index'),
    path('login/', manage.login),
] """

urlpatterns = [
    path('', views.index),
    path('ajax/<str:action>/',views.ajax),
]

""" 
    path('PlayerDetail/<str:name>/',views.PlayerDetail),
    path('kill/<int:bossid>/',views.kill),
    path('down_dkp/',views.down_dkp),
    path('down_epgp/',views.down_epgp),
    path('do_loot/',manage.do_loot),
    path('manage/',include(manage_patterns)), """