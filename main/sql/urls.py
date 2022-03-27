from django.urls import path
from . import views

app_name = "sql"
urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post, name='post'),
    path('queries/', views.queries, name='queries'),
    path('upload/', views.upload, name='views.upload'),
    path('sqlpage/', views.sqlpage, name='sqlpage'),
    path('homepage/', views.homepage, name='homepage'),
    path('insert/', views.insert, name='insert'),
    path('getit/', views.getit, name='getit')
]

