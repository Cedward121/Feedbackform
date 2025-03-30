from django.urls import path 
from . import views

urlpatterns = [
    path('chart', views.chart, name='chart'),
    path('time', views.time_dilation, name='time_dilation'),
    path('accurate', views.accurate, name='accurate'),
    path('latest', views.latest, name='latest'),
    ]