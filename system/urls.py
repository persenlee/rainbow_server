from django.urls import path
from system import api
from  system import  views

urlpatterns = [
    path('config', api.config),
    path('landing', views.landing_page),
    path('upload_token', api.upload_token)
]