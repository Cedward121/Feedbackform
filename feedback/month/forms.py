from django import forms
from datetime import date
from .models import EmployeeFeedback

class EmployeeFeedbackForm(forms.ModelForm):
    average_rating = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = EmployeeFeedback
        fields = [
            'Employee_name', 'Employee_email', 'Department',
            'Knowledge_of_Position', 'Quality_of_Work', 'Timely_Completion_of_Tasks',
            'Attendance_and_Punctuality', 'Communication_Skills', 'Accountability_and_Ownership',
            'Team_Collaboration_and_Coordination', 'Problem_Solving_and_Decision_Making',
            'Work_Consistency_and_Proactiveness', 'Ability_to_Handle_Pressure_Deadlines',
            'overall_performance', 'strengths_observed', 'areas_of_improvement'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.month_year = date.today().strftime('%Y-%m')  # Set month-year automatically
        if commit:
            instance.save()
        return instance
