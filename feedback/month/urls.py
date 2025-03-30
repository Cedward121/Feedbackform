from django.urls import path
from .views import employee_feedback_list

urlpatterns = [
    path('', employee_feedback_list, name='employee_feedback_list'),
]