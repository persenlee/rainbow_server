from django.urls import path
from system import api

urlpatterns = [
    path('config', api.config),
]