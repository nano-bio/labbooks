from __future__ import unicode_literals

from django.db import models
import cheminventory

# Create your models here.

class Experiment(models.Model):
    name = models.CharField(max_length = 20)
    persons = models.ManyToManyField('cheminventory.Person')

    def __str__(self):
        return self.name
