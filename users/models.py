
from django.db import models
# Create your models here.
class User(models.Model):
    First_name = models.TextField()
    Last_name = models.TextField()
    User_name = models.TextField(unique=True)
    password = models.TextField()

class Calendar(models.Model):
    event_date = models.DateTimeField(null=True)
    user_name = models.TextField()
    title = models.TextField()
    body = models.TextField(null=True)
    is_active = models.BooleanField()

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

