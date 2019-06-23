from django.conf.urls import url, include
from zeo import views

urlpatterns = [
    url('^$', views.index),
    url(r'^dashboard', views.task1),
    url(r'^logout', views.logout),
    url(r'^task/1', views.task1),
    url(r'^task/2', views.task2),
    url(r'^task/3', views.task3),
    url(r'^task/4', views.task4),
    url(r'^task/5', views.task5),
    url(r'^task/6', views.task6),
    url(r'^task/7', views.task7),
    url(r'^task/8', views.task8),
    url(r'^checkTask/(?P<id>[0-9]+)/?$', views.checkTask),
    url(r'^startTask', views.startTask),
    url(r'^', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    url(r'^', include('social_django.urls', namespace='social')),
]
