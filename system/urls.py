from django.urls import path
from system import api
from  system import  views

urlpatterns = [
    path('config', api.config),
    path('about', views.about_page),
    path('add_tag', views.add_tag_page),
    path('upload_token', api.upload_token)
]