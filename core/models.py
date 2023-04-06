from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    name = models.TextField(max_length=250, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return self.user.username