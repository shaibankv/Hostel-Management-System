from django.db import models
from student.models import Student

# Create your models here.

class Visitor(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    visitor_name = models.CharField(max_length=30)
    visit_date = models.DateField()
    visit_time = models.TimeField()
    visit_reason = models.TextField()

    def __str__(self):
        return f"{self.visitor_name} - {self.student}"
    
    

    