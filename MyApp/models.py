from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    # portfolio_site = models.URLField(blank=True)
    phone_number = models.CharField(max_length=14, default='+4915151234567', unique=True)
    email = models.EmailField(blank=False, unique=True)
    tokens = models.IntegerField(default=2)

    def __str__(self):
        return self.user.username
