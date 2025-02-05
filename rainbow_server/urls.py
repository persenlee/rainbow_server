"""rainbow_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image_browser/', include(('image_browser.urls', 'image_browser'), namespace='image_browser')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('feed/', include(('image_browser.urls', 'feed'), namespace='feed')),
    path('system/', include(('system.urls', 'system'), namespace='system')),
]
