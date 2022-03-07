from django.urls import path
from . import views

app_name = "sql"
urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post, name='post'),
    path('queries/', views.queries, name='queries'),
    path('upload/', views.upload, name='views.upload'),
]
