from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

SCANTYPES = (
    ('ES', 'Energyscan'),
    ('MS', 'Mass Spectrum'),
    ('TS', 'Temperature-Scan'),
    ('PS', 'Pressure-Scan'),
    ('OLD', 'Unknown (Old File)'),
)

POLARITIES = (
    ('NEG', 'Negative'),
    ('POS', 'Positive'),
    ('OLD', 'Unknown (Old File)'),
)

class Operator(models.Model):
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

class Measurement(models.Model):
    time = models.DateTimeField(auto_now = False, auto_now_add = False)
    tof_settings_file = models.CharField(max_length = 1500, verbose_name = 'TOF Settings File')
    data_filename = models.CharField(max_length=1500, verbose_name = 'Filename', default = 'D:\\Data\\')
    operator = models.ForeignKey('Operator')
    rating = models.IntegerField(blank = True, default = 3, null = True, validators = [MaxValueValidator(5), MinValueValidator(0)])
    scantype = models.CharField(max_length = 20, choices = SCANTYPES, default = 'MS')
    pressure_cs = models.FloatField(verbose_name = 'Pressure CS', default = float('4e-5'))
    pressure_pu1 = models.FloatField(verbose_name = 'Pressure PU1', default = float('3e-6'))
    pressure_pu2 = models.FloatField(verbose_name = 'Pressure PU2', default = float('1e-6'))
    pressure_ion = models.FloatField(verbose_name = 'Pressure ION', default = float('2e-8'))
    pressure_tof = models.FloatField(verbose_name = 'Pressure TOF', default = float('3e-7'))
    stag_pressure_he = models.FloatField(verbose_name = 'He Stagnation Pressure', default = 25)
    temperature_he = models.FloatField(verbose_name = 'He Temp', default = 9.0)
    nozzle_diameter = models.FloatField(default = 0.4)
    electron_energy_set = models.FloatField(blank = True, null = True, verbose_name = 'Electron Energy set on Power Supply (for MS)')
    real_electron_energy = models.FloatField(blank = True, null = True, verbose_name = 'Real Electron Energy (for MS)')
    ion_block = models.FloatField()
    pusher = models.FloatField()
    wehnelt = models.FloatField()
    extraction_1 = models.FloatField()
    extraction_2 = models.FloatField()
    deflector_1 = models.FloatField()
    deflector_2 = models.FloatField()
    filament_current = models.FloatField()
    trap_current = models.FloatField()
    housing_current = models.FloatField(blank = True, null = True)
    oven_1_temperature = models.FloatField(blank = True, null = True)
    oven_1_power = models.FloatField(blank = True, null = True)
    oven_2_temperature = models.FloatField(blank = True, null = True)
    oven_2_power = models.FloatField(blank = True, null = True)
    faraday_cup = models.FloatField(blank = True, null = True)
    flagged = models.BooleanField(default = False)
    substance = models.TextField(max_length=1500)
    polarity = models.CharField(max_length = 3, choices = POLARITIES, default = 'NEG')
    evaluated_by = models.CharField(max_length = 20, blank = True)
    evaluation_file = models.FileField(upload_to = 'clustof/evaluations/', blank = True, default = '')

    # this provides a link to the eval file in the admin interface

    def eval_file(self):
        if self.evaluation_file:
            return "<a href='%s'>Eval. file</a>" % (self.evaluation_file.url)
        else:
            return ''

    eval_file.allow_tags = True

    # same for the actual data file

    def data_file(self):
        return "<a href='%s'>Data file</a>" % ('/clustof/export/' + str(self.id))

    data_file.allow_tags = True

    def __unicode__(self):
        return u'%s, %s: %s ...' % (self.time, self.operator, self.substance[0:80])

    def elec_energy(self):
        if self.real_electron_energy is not None:
            ee = self.real_electron_energy
        elif self.electron_energy_set is not None:
            ee = self.electron_energy_set + self.ion_block
        else:
            ee = 1001

        # a little bit dirty. this means, either it cannot be computed
        # or somebody set it to 1234 (for ES) because it cannot be computed
        if ee > 1000:
            ee = '-'

        return ee

    class Meta:
        ordering = ['-time']
        get_latest_by = 'time'


class Comment(models.Model):
    measurement = models.ForeignKey('Measurement')
    operator = models.ForeignKey('Operator')
    time = models.DateTimeField(auto_now = False, auto_now_add = False)
    text = models.TextField(max_length=3000)

    def __unicode__(self):
        return u'%s, on %s' % (self.operator, self.time)

class JournalEntry(models.Model):
    time = models.DateTimeField(auto_now = False, auto_now_add = True)
    operator = models.ForeignKey('Operator')
    comment = models.TextField()
    attachment = models.FileField(upload_to = 'clustof/techjournal/', blank = True, default = '')

    def __unicode__(self):
        return u'%s, %s, %s: %s' % (self.id, self.time, self.operator, self.comment[:50])

    class Meta:
        ordering = ['-time']

class CurrentSetting(models.Model):
    tof_settings_file = models.CharField(max_length = 1500, verbose_name = 'TOF Settings File')
    tof_settings_file_time = models.DateTimeField()
    data_filename = models.CharField(max_length=1500, verbose_name = 'Filename', default = 'D:\\Data\\')
    data_filename_time = models.DateTimeField()
    pressure_cs = models.FloatField(verbose_name = 'Pressure CS', default = float('4e-5'))
    pressure_cs_time = models.DateTimeField()
    pressure_pu1 = models.FloatField(verbose_name = 'Pressure PU1', default = float('3e-6'))
    pressure_pu1_time = models.DateTimeField()
    pressure_pu2 = models.FloatField(verbose_name = 'Pressure PU2', default = float('1e-6'))
    pressure_pu2_time = models.DateTimeField()
    pressure_ion = models.FloatField(verbose_name = 'Pressure ION', default = float('2e-8'))
    pressure_ion_time = models.DateTimeField()
    pressure_tof = models.FloatField(verbose_name = 'Pressure TOF', default = float('3e-7'))
    pressure_tof_time = models.DateTimeField()
    temperature_he = models.FloatField(verbose_name = 'He Temperature', default = 9.0)
    temperature_he_time = models.DateTimeField()
    electron_energy_set = models.FloatField(blank = True, null = True, verbose_name = 'Electron Energy (for MS)')
    electron_energy_set_time = models.DateTimeField()
    ion_block = models.FloatField()
    ion_block_time = models.DateTimeField()
    pusher = models.FloatField()
    pusher_time = models.DateTimeField()
    wehnelt = models.FloatField()
    wehnelt_time = models.DateTimeField()
    extraction_1 = models.FloatField()
    extraction_1_time = models.DateTimeField()
    extraction_2 = models.FloatField()
    extraction_2_time = models.DateTimeField()
    deflector_1 = models.FloatField()
    deflector_1_time = models.DateTimeField()
    deflector_2 = models.FloatField()
    deflector_2_time = models.DateTimeField()
    filament_current = models.FloatField()
    filament_current_time = models.DateTimeField()
    trap_current = models.FloatField()
    trap_current_time = models.DateTimeField()
    oven_1_temperature = models.FloatField(blank = True, null = True)
    oven_1_temperature_time = models.DateTimeField()
    oven_1_power = models.FloatField(blank = True, null = True)
    oven_1_power_time = models.DateTimeField()
    oven_2_temperature = models.FloatField(blank = True, null = True)
    oven_2_temperature_time = models.DateTimeField()
    oven_2_power = models.FloatField(blank = True, null = True)
    oven_2_power_time = models.DateTimeField()
    polarity = models.CharField(max_length = 3, choices = POLARITIES, default = 'NEG')
    polarity_time = models.DateTimeField()
