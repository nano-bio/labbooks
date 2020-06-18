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
    gauge = models.ForeignKey(GaugeType, on_delete=models.CASCADE)
    usage_location = models.ForeignKey(UsageLocation, on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % (self.number)


class PressureGaugeUsageRecord(models.Model):
    gauge = models.ForeignKey(PressureGauge, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    usage_location = models.ForeignKey(UsageLocation, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return u'Gauge %s used at %s on %s' % (self.gauge.number, self.usage_location, self.date)


class Temperature(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    temp_sensor_1 = models.FloatField(blank=True, null=True, verbose_name='Teperature Prevacuum Room')
    temp_sensor_2 = models.FloatField(blank=True, null=True, verbose_name='Teperature Big Lab Room')
