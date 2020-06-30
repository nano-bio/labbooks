from django.db import models
import time
from django.conf import settings


class Operator(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return "{} {}.".format(self.firstname, self.lastname[:1])


class Measurement(models.Model):
    starttime = models.DateTimeField(auto_now=False, auto_now_add=False)
    datafile = models.FileField(upload_to='snowball/%Y/%m/%d/%H/%M/%S/', max_length=400)
    operator = models.ForeignKey('Operator', on_delete=models.PROTECT)
    he_temp = models.FloatField(verbose_name='He temp', default=float('9.5'))
    he_pres = models.FloatField(verbose_name='He pressure', default=float('20'))
    ee = models.FloatField(verbose_name='Electron Energy', default=float('70'))
    ee_2 = models.FloatField(verbose_name='Electron Energy IS2', default=float('70'))
    ec = models.FloatField(verbose_name='Electron Current', default=float('100'))
    ec_2 = models.FloatField(verbose_name='Electron Current IS2', default=float('100'))
    chan = models.FloatField(verbose_name='Channeltron Voltage', default=float('3500'))
    text = models.TextField(max_length=1500, verbose_name='Comment', blank=True)
    short_description = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return '{}, {},'.format(self.starttime, self.operator)

    def view_link(self):
        return "<a href='/vg/view/%s/'>View</a>" % (self.id)

    view_link.allow_tags = True

    def file_link(self):
        return u'<a href=\'%s\'>File</a>' % (self.datafile.url)

    file_link.allow_tags = True

    class Meta:
        ordering = ['-starttime']
        get_latest_by = 'starttime'


class JournalEntry(models.Model):
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    operator = models.ForeignKey('Operator', on_delete=models.PROTECT)
    comment = models.TextField()
    attachment = models.FileField(upload_to='snowball/techjournal/', blank=True, default='')
    written_notes = models.ImageField(blank=True, upload_to='snowball/techjournal/notes/')

    def __unicode__(self):
        return u'%s, %s, %s: %s' % (self.id, self.time, self.operator, self.comment[:50])

    def generate_filename(self):
        return settings.MEDIA_ROOT + 'snowball/techjournal/notes/' + str(time.time()) + '.png'

    class Meta:
        ordering = ['time']
        verbose_name_plural = "Journal Entries"


class Turbopump(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    service_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.name


class TurbopumpStatus(models.Model):
    pump = models.ForeignKey('Turbopump', on_delete=models.PROTECT)
    current = models.FloatField()
    date = models.DateField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = "Turbopump Status"

    def __unicode__(self):
        return '%s at %s: %s' % (self.pump.name, self.date, self.current)
