from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    account = models.CharField(max_length=30)
    passWord = models.CharField(max_length=40)
    eMail = models.EmailField()
    supermanagement = models.IntegerField(default=0)