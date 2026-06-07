from django.db import models




# Create your models here.

class Complaints(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    block = models.CharField(max_length=5, null=True, blank=True)
    room_no = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    complaint = models.CharField(max_length=40, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Solved', 'Solved'),('In Progress', 'In Progress')], default='Pending')

    def __str__(self):
        return f"{self.name} - {self.block} - {self.room_no}"



    


    
    
