from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from .forms import EmployeeFeedbackForm

def feedback_form(request):
    if request.method == "POST":
        form = EmployeeFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()

            # Email Subject & Recipient
            subject = "Employee Feedback Submission"
            recipient_email = feedback.Employee_email  # Send to Employee
            admin_email = "cedwardcheese4@gmail.com"  # Replace with your admin email

            # Context for HTML Email
            context = {
                'feedback': feedback,
            }

            # Render Email Template
            html_message = render_to_string('feedback_email.html', context)
            plain_message = strip_tags(html_message)  # Plain text version

            # Send email
            email = EmailMultiAlternatives(
                subject, plain_message, "cedwardcheese4@gmail.com", [recipient_email, admin_email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            return redirect('feedback_success')  # Redirect to success page

    else:
        form = EmployeeFeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})

def feedback_success(request):
    return render(request, 'feedback_success.html')


