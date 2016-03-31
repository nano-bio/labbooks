from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import time, datetime
from django.core.exeptions import ValidationError
from django.conf import settings

class Operator(models.Model):
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

#class Measuremente(models.Model):
   #time = models.DateTimeField(auto_now = false, auto_now_add = False)
   # data_filename = models.CharField(max_length = 1500, verbose_name
