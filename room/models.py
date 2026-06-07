from django.db import models

# Create your models here.
class Room(models.Model):
    block = models.CharField(max_length=5)
    room_no = models.CharField(max_length=10)
    capacity = models.IntegerField()

    class Meta:
        unique_together = ['block', 'room_no']

    @property
    def available_space(self):
        return self.capacity - self.student_set.count()

    def __str__(self):
        return f"{self.block} - {self.room_no}"
    
