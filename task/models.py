from django.db import models


# Create your models here.
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    taskName = models.CharField(max_length=40)
    projectName = models.CharField(max_length=125)
    status = models.IntegerField(default=0)
    creator = models.CharField(max_length=20)
    createTime = models.CharField(max_length=100, default=None)
