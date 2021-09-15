import datetime
import re
from operator import attrgetter

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe

from cheminventory import models as cheminventory_models
from journal.models import BasicJournalEntry

SCANTYPES = (
    ('ES', 'Energyscan'),
    ('MS', 'Mass Spectrum'),
    ('TS', 'Temperature-Scan'),
    ('PS', 'Pressure-Scan'),
    ('LS', 'Laser-Scan'),
    ('OLD', 'Unknown (Old File)'),
)

POLARITIES = (
    ('NEG', 'Negative'),
    ('POS', 'Positive'),
    ('OLD', 'Unknown (Old File)'),
)


class Operator(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return u'%s %s' % (self.firstname, self.lastname)


class Measurement(models.Model):
    time = models.DateTimeField(auto_now=False, auto_now_add=False)
    tof_settings_file = models.CharField(max_length=1500, verbose_name='TOF Settings File')
    laser_power_file = models.FileField(
        upload_to='clustof/powerfiles/', blank=True,
        verbose_name='Laser Power Measurement File')
    cluster_size_distribution = models.FileField(
        upload_to='clustof/clusterSizeDistribution/',
        blank=True, null=True)
    data_filename = models.CharField(max_length=1500, verbose_name='Filename', default='D:\\Data\\')
    operator = models.ForeignKey('Operator', related_name='op1',
                                 on_delete=models.PROTECT)
    operator2 = models.ForeignKey('Operator', related_name='op2', blank=True, null=True,
                                  on_delete=models.PROTECT)
    operator3 = models.ForeignKey('Operator', related_name='op3', blank=True, null=True,
                                  on_delete=models.PROTECT)
    rating = models.IntegerField(blank=True, default=3, null=True,
                                 validators=[MaxValueValidator(5), MinValueValidator(0)])
    scantype = models.CharField(max_length=20, choices=SCANTYPES, default='MS')
    pressure_cs = models.FloatField(verbose_name='Pressure CS', default=float('4e-5'))
    pressure_pu1 = models.FloatField(verbose_name='Pressure PU1', default=float('3e-6'))
    pressure_pu2 = models.FloatField(verbose_name='Pressure PU2', default=float('1e-6'))
    pressure_pu3 = models.FloatField(verbose_name='Pressure PU3', default=float('1e-6'))
    pressure_ion = models.FloatField(verbose_name='Pressure ION', default=float('2e-8'))
    pressure_tof = models.FloatField(verbose_name='Pressure TOF', default=float('3e-7'))
    laser_timing = models.IntegerField(blank=True, null=True)
    stag_pressure_he = models.FloatField(verbose_name='He Stagnation Pressure', default=25)
    temperature_he = models.FloatField(verbose_name='He Temp', default=9.0)
    nozzle_diameter = models.FloatField(default=5)
    electron_energy_set = models.FloatField(
        blank=True, null=True,
        verbose_name='Electron Energy set on Power Supply (for MS)')
    real_electron_energy = models.FloatField(blank=True, null=True, verbose_name='Real Electron Energy (for MS)')
    ion_block = models.FloatField()
    pusher = models.FloatField()
    wehnelt = models.FloatField()
    extraction_1 = models.FloatField(blank=True, null=True)
    extraction_1_left = models.FloatField(blank=True, null=True)
    extraction_1_right = models.FloatField(blank=True, null=True)
    extraction_2 = models.FloatField()
    deflector_1 = models.FloatField(verbose_name='Deflector oben/unten')
    deflector_2 = models.FloatField(verbose_name='Deflector links/rechts')
    filament_current = models.FloatField()
    trap_current = models.FloatField()
    housing_current = models.FloatField(blank=True, null=True)
    oven_1_temperature = models.FloatField(blank=True, null=True)
    oven_1_power = models.FloatField(blank=True, null=True)
    oven_2_temperature = models.FloatField(blank=True, null=True)
    oven_2_power = models.FloatField(blank=True, null=True)
    faraday_cup = models.FloatField(blank=True, null=True)
    flagged = models.BooleanField(default=False)
    substance = models.TextField(max_length=1500, verbose_name='Comment')
    chem_pu1_oven = models.ForeignKey(
        cheminventory_models.Chemical,
        related_name='chem_pu1_oven',
        blank=True, null=True,
        verbose_name='Chemical PU1 Oven',
        on_delete=models.PROTECT)
    chem_pu1_gas = models.ForeignKey(
        cheminventory_models.Chemical,
        related_name='chem_pu1_gas',
        blank=True, null=True,
        verbose_name='Chemical PU1 Gas',
        on_delete=models.PROTECT)
    chem_pu2_oven = models.ForeignKey(
        cheminventory_models.Chemical,
        related_name='chem_pu2_oven',
        blank=True, null=True,
        verbose_name='Chemical PU2 Oven',
        on_delete=models.PROTECT)
    chem_pu2_gas = models.ForeignKey(
        cheminventory_models.Chemical,
        related_name='chem_pu2_gas',
        blank=True, null=True,
        verbose_name='Chemical PU2 Gas',
        on_delete=models.PROTECT)
    is_inlet_gas = models.ForeignKey(
        cheminventory_models.Chemical,
        related_name='is_inlet_gas',
        blank=True, null=True,
        verbose_name='Ion Source Inlet Gas',
        on_delete=models.PROTECT)
    polarity = models.CharField(max_length=3, choices=POLARITIES, default='NEG')
    evaluated_by = models.CharField(max_length=20, blank=True)
    evaluation_file = models.FileField(upload_to='clustof/evaluations/', blank=True, default='')
    marked = models.BooleanField(default=False)
    lis_filament_current = models.FloatField(verbose_name="Filament current", blank=True, null=True)
    lis_trap_current = models.FloatField(verbose_name="Trap current", blank=True, null=True)
    lis_deflector_y = models.FloatField(verbose_name="Deflector Y", blank=True, null=True)
    lis_deflector_z = models.FloatField(verbose_name="Deflector Z", blank=True, null=True)
    lis_ion_block = models.FloatField(verbose_name="Ion block", blank=True, null=True)
    lis_electron_energy = models.FloatField(verbose_name="Electron energy", blank=True, null=True)

    # this provides a link to the eval file in the admin interface
    def eval_file(self):
        if self.evaluation_file:
            return mark_safe("<a href='{}'>Eval. file</a>".format(self.evaluation_file.url))
        else:
            return ''

    # same for the actual data file
    def data_file(self):
        return mark_safe("<a href='/clustof/export/{}'>Data file</a>".format(self.id))

    def __str__(self):
        return '{}, {}: {} ...'.format(self.time, self.operator, self.substance[0:80])

    def elec_energy(self) -> str:
        if self.real_electron_energy is not None:
            ee = self.real_electron_energy
        elif self.electron_energy_set is not None:
            ee = self.electron_energy_set + self.ion_block
        else:
            ee = 1001

        # a little bit dirty. this means, either it cannot be computed
        # or somebody set it to 1234 (for ES) because it cannot be computed
        if ee > 1000:
            return '-'

        return "{:.1f}".format(ee)

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
    measurement = models.ForeignKey('Measurement', on_delete=models.PROTECT)
    operator = models.ForeignKey('Operator', on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)
    text = models.TextField(max_length=3000)

    def __str__(self):
        return u'%s, on %s' % (self.operator, self.time)


class JournalEntry(BasicJournalEntry):
    pass


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

    def __str__(self):
        return '%s at %s: %s' % (self.pump.name, self.date, self.current)


class VacuumStatus(models.Model):
    time = models.IntegerField()
    g1 = models.FloatField(blank=True, null=True)
    g2 = models.FloatField(blank=True, null=True)
    g3 = models.FloatField(blank=True, null=True)
    g4 = models.FloatField(blank=True, null=True)
    g5 = models.FloatField(blank=True, null=True)
    g6 = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Vacuum Status"

    def __str__(self):
        return u'Pressures at %s' % (datetime.datetime.fromtimestamp(self.time).strftime('%c'))
