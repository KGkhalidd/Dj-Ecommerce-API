from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    reset_password_expires = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"