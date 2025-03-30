from .views import *
from django.urls import path, include
 
urlpatterns = [
    path('', home, name='home'),
    path('api/get_GFG/', get_hotel, name='get_hotel'),
]
