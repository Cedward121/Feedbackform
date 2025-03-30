from django.shortcuts import render
from .models import EmployeeFeedback
from datetime import datetime

def employee_feedback_list(request):
    employees = EmployeeFeedback.objects.values_list('Employee_name', flat=True).distinct()

    employee_name = request.GET.get('employee_name')
    month_year = request.GET.get('month_year', datetime.today().strftime('%Y-%m'))  # Default to current month

    feedbacks = EmployeeFeedback.objects.filter(month_year=month_year)
    if employee_name:
        feedbacks = feedbacks.filter(Employee_name=employee_name)

    return render(request, 'employee_feedback_list.html', {
        'feedbacks': feedbacks,
        'employees': employees,
        'selected_employee': employee_name,
        'selected_month': month_year
    })
