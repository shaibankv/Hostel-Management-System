from django.db import models
from student.models import Student

# Create your models here.

class Presence(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date_out = models.DateField()
    time_out = models.TimeField()
    date_in = models.DateField(null=True, blank=True)
    time_in = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length = 10)
    reason = models.TextField()

    def __str__(self):
        return self.student.name
