from django.db import models

class EmployeeFeedback(models.Model):
    EMPLOYEE_RATINGS = [(i, str(i)) for i in range(1, 6)]  
    PERFORMANCE_CHOICES = [
        ('Needs Improvement', 'Needs Improvement'),
        ('Satisfactory', 'Satisfactory'),
        ('Good', 'Good'),
        ('Very Good', 'Very Good'),
        ('Excellent', 'Excellent'),
    ]

    Employee_name = models.CharField(max_length=255)
    Employee_email = models.EmailField(max_length=255, blank=True, null=True)
    Department = models.CharField(max_length=100)
    feedback_month = models.DateField()  

    Knowledge_of_Position = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Quality_of_Work = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Timely_Completion_of_Tasks = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Attendance_and_Punctuality = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Communication_Skills = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Accountability_and_Ownership = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Team_Collaboration_and_Coordination = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Problem_Solving_and_Decision_Making = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Work_Consistency_and_Proactiveness = models.IntegerField(choices=EMPLOYEE_RATINGS)
    Ability_to_Handle_Pressure_Deadlines = models.IntegerField(choices=EMPLOYEE_RATINGS)

    strengths_observed = models.TextField(blank=True, null=True)
    areas_of_improvement = models.TextField(blank=True, null=True)
    overall_performance = models.CharField(max_length=20, choices=PERFORMANCE_CHOICES, default='Satisfactory')

    class Meta:
        unique_together = ('Employee_email', 'feedback_month')  # Ensure monthly uniqueness

    def average_rating(self):
        """Calculate the average of all rating fields."""
        rating_fields = [
            self.Knowledge_of_Position,
            self.Quality_of_Work,
            self.Timely_Completion_of_Tasks,
            self.Attendance_and_Punctuality,
            self.Communication_Skills,
            self.Accountability_and_Ownership,
            self.Team_Collaboration_and_Coordination,
            self.Problem_Solving_and_Decision_Making,
            self.Work_Consistency_and_Proactiveness,
            self.Ability_to_Handle_Pressure_Deadlines,
        ]
        return round(sum(rating_fields) / len(rating_fields), 2)

    def __str__(self):
        return f"{self.Employee_name} - {self.overall_performance} ({self.feedback_month})"
