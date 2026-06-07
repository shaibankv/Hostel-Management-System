from django.db import models
from accounts.models import UserList
from room.models import Room

from django.core.exceptions import ValidationError

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(UserList, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)
    reg_number=models.CharField(max_length=25, unique=True)
    dob = models.DateField("Date of Birth")
    course = models.CharField(max_length=20)
    year = models.IntegerField()

    hostel_fee = models.IntegerField()

    phone = models.CharField(max_length=15,default='+91')
    email = models.EmailField()
    home_address = models.TextField()

    guardian_name = models.CharField(max_length=30)
    guardian_phone = models.CharField(max_length=15,default='+91')
    guardian_email = models.EmailField()

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    def clean(self):
        if self.room:
            student_count = Student.objects.filter(room=self.room).exclude(id=self.id).count()
            if student_count >= self.room.capacity:
                raise ValidationError("This room is already full.")

    photo = models.ImageField(upload_to='students_photo/')

    id_proof = models.FileField(upload_to='id_proof/')

    def __str__(self):
        return f"{self.name} ({self.reg_number})"
    
    



