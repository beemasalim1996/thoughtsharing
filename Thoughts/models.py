
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustUser(AbstractUser):
    logo = models.ImageField(
        upload_to='logo/', blank=True, null=True)


class Thoughts(models.Model):
    Thought = models.CharField(max_length=255)
    ThoughtImportant = models.BooleanField(default=False)
    userId = models.ForeignKey(
        CustUser, on_delete=models.CASCADE, blank=True, null=True)

    addOnDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)



