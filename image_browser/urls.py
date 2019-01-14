from django.urls import path,re_path
from django.views.generic.base import RedirectView
from image_browser import views

urlpatterns = [
    path('', views.home, name='home'),
    path('image_list/', views.image_list),
    path('report_page/', views.report_page),
    re_path(r'star/$', views.star),
    re_path(r'add_tag/$', views.add_tag)
    # path(r'^favicon\.ico$', RedirectView.as_view(url=r'static/images/favicon.ico'))
]