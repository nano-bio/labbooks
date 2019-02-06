from django.db import models

from cheminventory.models import Person, UsageLocation

MODUS = (
    ('PIR', 'Pirani'),
    ('FULL', 'Full Range'),
    ('COLD', 'Cold Cathode'),
    ('UNKN', 'Unknown')
)

class GaugeType(models.Model):
    company = models.CharField(max_length=30)
    type = models.CharField(max_length=50)
    modus = models.CharField(max_length=4, choices=MODUS)

    def __unicode__(self):
        return u'%s (%s, %s)' % (self.get_modus_display(), self.company, self.type)

class PressureGauge(models.Model):
    number = models.CharField(max_length=4)
    gauge = models.ForeignKey(GaugeType)
    usage_location = models.ForeignKey(UsageLocation)

    def __unicode__(self):
        return u'%s' % (self.number)


class PressureGaugeUsageRecord(models.Model):
    gauge = models.ForeignKey(PressureGauge)
    date = models.DateField()
    user = models.ForeignKey(Person)
    usage_location = models.ForeignKey(UsageLocation)
    comment = models.CharField(max_length = 100, blank = True)

    def __unicode__(self):
        return u'Gauge %s used at %s on %s' % (self.gauge.number, self.usage_location, self.date)
