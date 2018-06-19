from django.db import models

class Container (models.Model):
    name = models.CharField(max_length=30)

class Objects (models.Model):
    name = models.CharField(max_length=30)
    file = models.FileField()
"""
class Files(models.Model):
    container=models.CharField (max_length=30)
    object=models.CharField (max_length=30)
    token = models.CharField(max_length=100, default="a6803dedfad548258fe252a7621492af")
    location = models.CharField(max_length=30, default="download")

"""
# Create your models here.
