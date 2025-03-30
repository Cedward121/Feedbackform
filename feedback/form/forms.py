from django import forms
from .models import EmployeeFeedback

class EmployeeFeedbackForm(forms.ModelForm):
    average_rating = forms.FloatField(
        required=False,  # Not required because it's calculated dynamically
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  # Make it read-only
    )

    class Meta:
        model = EmployeeFeedback
        fields = [
            'Employee_name', 'Employee_email', 'Department', 'Knowledge_of_Position',
            'Quality_of_Work', 'Timely_Completion_of_Tasks', 'Attendance_and_Punctuality',
            'Communication_Skills', 'Accountability_and_Ownership', 'Team_Collaboration_and_Coordination',
            'Problem_Solving_and_Decision_Making', 'Work_Consistency_and_Proactiveness',
            'Ability_to_Handle_Pressure_Deadlines', 'overall_performance', 'strengths_observed',
            'areas_of_improvement', 'average_rating'  
        ]

    def clean(self):
        cleaned_data = super().clean()

        # Get all rating fields
        ratings = [
            cleaned_data.get('Knowledge_of_Position', 0),
            cleaned_data.get('Quality_of_Work', 0),
            cleaned_data.get('Timely_Completion_of_Tasks', 0),
            cleaned_data.get('Attendance_and_Punctuality', 0),
            cleaned_data.get('Communication_Skills', 0),
            cleaned_data.get('Accountability_and_Ownership', 0),
            cleaned_data.get('Team_Collaboration_and_Coordination', 0),
            cleaned_data.get('Problem_Solving_and_Decision_Making', 0),
            cleaned_data.get('Work_Consistency_and_Proactiveness', 0),
            cleaned_data.get('Ability_to_Handle_Pressure_Deadlines', 0),
        ]

        # Calculate average rating
        cleaned_data['average_rating'] = round(sum(ratings) / len(ratings), 2)

        return cleaned_data

    
