from django.db import models
from accounts.models import UserList

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(UserList, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length = 30)
    role = models.CharField(max_length = 20)
    phone = models.CharField(max_length = 14, default='+91')
    email = models.EmailField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    shift = models.CharField(max_length = 25)
    block = models.CharField(max_length = 5, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
    