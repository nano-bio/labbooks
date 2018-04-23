from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import re, time, datetime
from django.core.exceptions import ValidationError
from django.conf import settings
from cheminventory import models as cheminventory_models
from operator import attrgetter

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
    laser_power_file = models.FileField(upload_to = 'clustof/powerfiles/', blank=True, verbose_name = 'Laser Power Measurement File')
    data_filename = models.CharField(max_length=1500, verbose_name = 'Filename', default = 'D:\\Data\\')
    operator = models.ForeignKey('Operator', related_name = 'op1')
    operator2 = models.ForeignKey('Operator', related_name = 'op2', blank = True, null = True)
    operator3 = models.ForeignKey('Operator', related_name = 'op3', blank = True, null = True)
    rating = models.IntegerField(blank = True, default = 3, null = True, validators = [MaxValueValidator(5), MinValueValidator(0)])
    scantype = models.CharField(max_length = 20, choices = SCANTYPES, default = 'MS')
    pressure_cs = models.FloatField(verbose_name = 'Pressure CS', default = float('4e-5'))
    pressure_pu1 = models.FloatField(verbose_name = 'Pressure PU1', default = float('3e-6'))
    pressure_pu2 = models.FloatField(verbose_name = 'Pressure PU2', default = float('1e-6'))
    pressure_ion = models.FloatField(verbose_name = 'Pressure ION', default = float('2e-8'))
    pressure_tof = models.FloatField(verbose_name = 'Pressure TOF', default = float('3e-7'))
    laser_timing = models.IntegerField(blank=True, null=True)
    stag_pressure_he = models.FloatField(verbose_name = 'He Stagnation Pressure', default = 25)
    temperature_he = models.FloatField(verbose_name = 'He Temp', default = 9.0)
    nozzle_diameter = models.FloatField(default = 5)
    electron_energy_set = models.FloatField(blank = True, null = True, verbose_name = 'Electron Energy set on Power Supply (for MS)')
    real_electron_energy = models.FloatField(blank = True, null = True, verbose_name = 'Real Electron Energy (for MS)')
    ion_block = models.FloatField()
    pusher = models.FloatField()
    wehnelt = models.FloatField()
    extraction_1 = models.FloatField(blank = True, null = True)
    extraction_1_left = models.FloatField(blank = True, null = True)
    extraction_1_right = models.FloatField(blank = True, null = True)
    extraction_2 = models.FloatField()
    deflector_1 = models.FloatField(verbose_name = 'Deflector oben/unten')
    deflector_2 = models.FloatField(verbose_name = 'Deflector links/rechts')
    filament_current = models.FloatField()
    trap_current = models.FloatField()
    housing_current = models.FloatField(blank = True, null = True)
    oven_1_temperature = models.FloatField(blank = True, null = True)
    oven_1_power = models.FloatField(blank = True, null = True)
    oven_2_temperature = models.FloatField(blank = True, null = True)
    oven_2_power = models.FloatField(blank = True, null = True)
    faraday_cup = models.FloatField(blank = True, null = True)
    flagged = models.BooleanField(default = False)
    substance = models.TextField(max_length=1500, verbose_name = 'Comment')
    chem_pu1_oven = models.ForeignKey(cheminventory_models.Chemical, related_name = 'chem_pu1_oven', blank = True, null = True, verbose_name = 'Chemical PU1 Oven')
    chem_pu1_gas = models.ForeignKey(cheminventory_models.Chemical, related_name = 'chem_pu1_gas', blank = True, null = True, verbose_name = 'Chemical PU1 Gas')
    chem_pu2_oven = models.ForeignKey(cheminventory_models.Chemical, related_name = 'chem_pu2_oven', blank = True, null = True, verbose_name = 'Chemical PU2 Oven')
    chem_pu2_gas = models.ForeignKey(cheminventory_models.Chemical, related_name = 'chem_pu2_gas', blank = True, null = True, verbose_name = 'Chemical PU2 Gas')
    is_inlet_gas = models.ForeignKey(cheminventory_models.Chemical, related_name = 'is_inlet_gas', blank = True, null = True, verbose_name = 'Ion Source Inlet Gas')
    polarity = models.CharField(max_length = 3, choices = POLARITIES, default = 'NEG')
    evaluated_by = models.CharField(max_length = 20, blank = True)
    evaluation_file = models.FileField(upload_to = 'clustof/evaluations/', blank = True, default = '')
    marked = models.BooleanField(default = False)

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


    def chems(self):
        chems = [self.chem_pu1_oven, self.chem_pu1_gas, self.chem_pu2_oven, self.chem_pu2_gas, self.is_inlet_gas]
        chems_used = filter(None, chems)
        chem_string = u' '.join(map(attrgetter('chemical_formula'), chems_used))
        return chem_string

    def clean(self):
        # cleaning method. first thing, check if file extension is there
        try:
            fn = self.data_filename.split('\\')[2]
        except IndexError:
            raise ValidationError('Something is odd about this filename. Did you forget the path?')

        if re.match('^DataFile_20[0-2][0-9].[0|1][0-9].[0-3][0-9]-[0-9]{2}h[0-9]{2}m[0-9]{2}s_AS$', fn):
            # if this matches, its a TOF-file, but without the extension
            # --> somebody (Paul) forgot the file extension.
            self.data_filename = self.data_filename + '.h5'

        # further sanity checks
        # polarity negative -> no positive lens values:
        if self.polarity == 'NEG':
            if self.ion_block > 0:
                raise ValidationError('Ion block should be negative when measuring anions. Please double check!')

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
    written_notes = models.ImageField(blank = True, upload_to = 'clustof/techjournal/notes/')

    def __unicode__(self):
        return u'%s, %s, %s: %s' % (self.id, self.time, self.operator, self.comment[:50])

    def generate_filename(self):
        return settings.MEDIA_ROOT + 'clustof/techjournal/notes/' + str(time.time()) + '.png'

    class Meta:
        ordering = ['-time']
        verbose_name_plural = "Journal Entries"

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

class Turbopump(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank = True)
    purchase_date = models.DateField(auto_now_add = False, auto_now = False, blank = True, null = True)
    service_date = models.DateField(auto_now_add = False, auto_now = False, blank = True, null = True)

    def __unicode__(self):
       return self.name

class TurbopumpStatus(models.Model):
    pump = models.ForeignKey('Turbopump')
    current = models.FloatField()
    date = models.DateField(auto_now_add = True, auto_now = False)

    class Meta:
        verbose_name_plural = "Turbopump Status"

    def __unicode__(self):
        return '%s at %s: %s' % (self.pump.name, self.date, self.current)

class VacuumStatus(models.Model):
    time = models.IntegerField()
    g1 = models.FloatField(blank = True, null = True)
    g2 = models.FloatField(blank = True, null = True)
    g3 = models.FloatField(blank = True, null = True)
    g4 = models.FloatField(blank = True, null = True)
    g5 = models.FloatField(blank = True, null = True)
    g6 = models.FloatField(blank = True, null = True)
    temperature = models.FloatField(blank = True, null = True)

    class Meta:
        verbose_name_plural = "Vacuum Status"

    def __unicode__(self):
        return u'Pressures at %s' % (datetime.datetime.fromtimestamp(self.time).strftime('%c')) 
