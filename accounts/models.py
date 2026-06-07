from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserList(AbstractUser):
    ROLE_CHOICES = (
        ('Admin','Admin'),
        ('Warden','Warden'),
        ('Staff','Staff'),
        ('Student','Student'),
    )    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    plain_password = models.CharField(max_length=128, null=True, blank=True)
    def __str__(self):
        return self.username
