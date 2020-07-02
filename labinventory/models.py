from django.db import models

from cheminventory.models import Person, UsageLocation

MODE = (
    ('PIR', 'Pirani'),
    ('FULL', 'Full Range'),
    ('COLD', 'Cold Cathode'),
    ('UNKN', 'Unknown')
)


class GaugeType(models.Model):
    company = models.CharField(max_length=30)
    type = models.CharField(max_length=50)
    mode = models.CharField(max_length=4, choices=MODE)

    def __str__(self):
        return "{} ({}, {})".format(self.get_mode_display(), self.company, self.type)


class PressureGauge(models.Model):
    number = models.CharField(max_length=4)
    gauge = models.ForeignKey(GaugeType, on_delete=models.CASCADE)
    usage_location = models.ForeignKey(UsageLocation, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.number)


class PressureGaugeUsageRecord(models.Model):
    gauge = models.ForeignKey(PressureGauge, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    usage_location = models.ForeignKey(UsageLocation, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "Gauge {} used at {} on {}".format(self.gauge.number, self.usage_location, self.date)


class Temperature(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    temp_sensor_1 = models.FloatField(blank=True, null=True, verbose_name='Temperature Prevacuum Room')
    temp_sensor_2 = models.FloatField(blank=True, null=True, verbose_name='Temperature Big Lab Room')


ALARM_TYPES = (
    ('poweralarm', 'Power alarm'),
    ('tempalarm', 'Temperature alarm'),
)


class Alarm(models.Model):
    persons = models.ManyToManyField('cheminventory.Person')
    type = models.CharField(max_length=10, choices=ALARM_TYPES)

    def __str__(self):
        return self.type
