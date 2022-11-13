from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser, models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

class CurriculumVitae(models.Model):
    cv = models.FileField(null=True, upload_to="curr_vits/")
    title = models.CharField(max_length=50, null=True)
    def save(self): # new
        super().save()