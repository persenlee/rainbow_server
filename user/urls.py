from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='index'),
    path('register',views.register_page),
    path('sign_up',views.sign_up),
    path('sign_in', views.sign_in),
    path('send_mail', views.get_mail_code),

]