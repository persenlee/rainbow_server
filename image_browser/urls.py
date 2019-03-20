from django.urls import path, re_path
from image_browser import views, api

urlpatterns = [
    # path('', views.home, name='home'),
    # path('image_list/', views.image_list),
    # path('report_page/', views.report_page),
    # re_path(r'star/$', views.star),
    # re_path(r'add_tag/$', views.add_tag),
    path('feeds', api.feeds),
    path('like', api.like),
    path('tags', api.tags),
    path('report', api.report),
]
