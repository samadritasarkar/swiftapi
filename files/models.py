from django.db import models

class Container (models.Model):
    name = models.CharField (max_length=30)
    def __str__(self):
        return self.name

class Object (models.Model):

    file = models.FileField()
    def __str__(self):
        return self.name

