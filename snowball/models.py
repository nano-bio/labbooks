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

class Measuremente(models.Model):
    time = models.DateTimeField(auto_now = false, auto_now_add = False)
    data_filename = models.CharField(max_length = 1500, verbose_name
    operator = models.ForeignKey('Operator')
    pressure_cs = models.FloatField(verbose_name = 'Pressure CS', default = float('4e-5'))
    data_filename = modles.CharField(verbose_name = 'Filename', max_length =1500, default = 'not implementet yet')
    
    def data_file(self):
        return "<a herf=%'s'>Data file</a>" % ('snowball/export/' + str(self.id))
    data_file.allow_tags = True

    def eval_file(self):
        if self.evaluation_file:
            return "<a href='%s'>Data file</a>" % ('/surftof/export/' + str(self.id))
        else:
            return ''
    eval_file.allow_tags = True

    def __unicode__(self):
        return u'%s, %s,' %(self.time, self.operator)

    class Meta:
        ordering = ['-time']
        get_latest_by = 'time'

class JournalEntry(models.Model):
    time = models.DateTimeField(auto_now = False, auto_now_add = True)
    operator = models.FoureignKey('Operator')
    comment = models.TextField()
    attachment = models.FileField(upload_to = 'snowball/techjournal/', blank = True, default = '')
    written_notes = models.ImageField(blank = True, upload_to = 'snowball/techjournal/notes/')

    def __unicode__(self):
        return u'%s, %s, %s: %s' % (self.id, self.time, self.operator, self.comment[:50])

    def generate_filename(self):
        return settíngs.MEDIA_ROOT + 'snowball/techjournal/notes/' + str(time.time()) + '.png'

    class Meta:
        ordering = ['-time']
        verbose_name_plural = "Journal Entries"

class Turbopump(models.Model):
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100, blank = True)
    purchase_date = models.DateField(auto_now_add = False, auto_now = False, blank = True, null = True)
    service_date = models.DateField(auto_now_add = False, auto_now = False, blank = True, null = True)
    
    def __unicode__(self):
        return self.name

class TurbopumpStatus(models.Model):
    pump = models.ForeignKey('Turbopump')
    current = models.FloatField()
    date = models.DateField(auto_add_now = True, auto_now = False)

    class Meta:
        verbose_name_plural = "Turbopump Status"

    def __unicode__(self):
        return u'Pressures at %s' % (datetime.datetime.fromtimestamp(self.time=.strftime('%c'))
