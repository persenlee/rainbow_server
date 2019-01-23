from django.urls import path
from user import views
from user import api

urlpatterns = [
    path('', views.login_page, name='index'),
    path('register', views.register_page),
    path('sign_up', views.sign_up),
    path('sign_in', views.sign_in),
    path('send_mail', views.get_mail_code),

    path('login', api.login),
    path('signup', api.register),
    path('mail_code', api.mail_code),
    path('email_used', api.email_used),
    path('profile', api.profile),
    path('likes', api.likes),

]
