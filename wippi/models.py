from django.db import models
from cheminventory import models as cheminventory_models

ENERGYSCAN = 'ES'
MASSSCAN = 'MS'

SCANTYPES = (
    (ENERGYSCAN, 'Energyscan'),
    (MASSSCAN, 'Massscan'),
)

POLARITIES = (
    ('NEG', 'Negative'),
    ('POS', 'Positive'),
)

class Operator(models.Model):
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

class Measurement(models.Model):
    operator = models.ForeignKey('Operator')
    time = models.DateTimeField(auto_now = False, auto_now_add = False)
    datafile = models.FileField(upload_to = 'wippi/%Y/%m/%d/%H/%M/%S/', max_length = 400)
    scantype = models.CharField(max_length = 20, choices = SCANTYPES, default = ENERGYSCAN)
    gatetime = models.FloatField(blank = True, null = True)
    polarity = models.CharField(max_length = 3, choices = POLARITIES, default = 'NEG')
    electron_energy = models.FloatField(blank = True, null = True, verbose_name = 'Electron Energy (for MS)')
    ion_energy = models.FloatField(blank = True, null = True)
    substance = models.ForeignKey(cheminventory_models.Chemical, null = True)
    substance_comment = models.CharField(max_length = 200, blank = True)
    fragment = models.CharField(blank = True, max_length = 200)
    description = models.CharField(max_length = 200)
    channeltron_1 = models.FloatField(default = 5.8, verbose_name = 'Channeltron 1', blank = True, null = True)
    channeltron_2 = models.FloatField(verbose_name = 'Channeltron 2', blank = True, null = True)
    ue = models.FloatField(verbose_name = 'Ue', blank = True, null = True)
    ue_fine = models.FloatField(verbose_name = 'Ue fine', blank = True, null = True)
    oven_temperature = models.PositiveIntegerField(blank = True, null = True)
    chamber_temperature = models.PositiveIntegerField(default = 90, blank = True, null = True)
    faraday_current = models.PositiveIntegerField(blank = True, null = True)
    filament_current = models.FloatField(default = 2.36)
    emission = models.PositiveIntegerField(blank = True, null = True)
    energy_resolution = models.FloatField(blank = True, null = True)
    mass_resolution = models.FloatField(verbose_name = 'Mass Resolution (Quadrupole)', default = 25, blank = True, null = True)
    pressure_monochromator = models.CharField(max_length = 7, default = '2e-6', verbose_name = 'Pressure MC (mbar)')
    pressure_pickup = models.CharField(max_length = 7, verbose_name = 'Pressure Pickup (mbar)', blank = True)
    pressure_cs = models.CharField(max_length = 7, verbose_name = 'Pressure Cluster Source (mbar)', blank = True)
    base_pressure = models.CharField(max_length = 7, verbose_name = 'Base Pressure Cluster Source (mbar)', blank = True)
    background_pressure = models.FloatField(blank = True, null = True, verbose_name = 'Background Pressure in MC (mbar)')
    anode = models.FloatField(blank = True, null = True)
    def_a = models.FloatField(blank = True, null = True)
    def_i = models.FloatField(blank = True, null = True)
    optics_inside = models.FloatField(blank = True, null = True)
    optics_outside = models.FloatField(blank = True, null = True)
    field_axis = models.FloatField(blank = True, null = True)
    coil_voltage_xy = models.FloatField(blank = True, null = True, verbose_name = 'Coil Voltage XY')
    coil_voltage_xz = models.FloatField(blank = True, null = True, verbose_name = 'Coil Voltage XZ')
    coil_voltage_yz = models.FloatField(blank = True, null = True, verbose_name = 'Coil Voltage YZ')
    coil_current_xy = models.FloatField(blank = True, null = True, verbose_name = 'Coil Current XY')
    coil_current_xz = models.FloatField(blank = True, null = True, verbose_name = 'Coil Current XZ')
    coil_current_yz = models.FloatField(blank = True, null = True, verbose_name = 'Coil Current YZ')
    lens_1a = models.FloatField(blank = True, null = True)
    lens_1b = models.FloatField(blank = True, null = True)
    lens_1c = models.FloatField(blank = True, null = True)
    lens_A1 = models.FloatField(blank = True, null = True)
    lens_L2 = models.FloatField(blank = True, null = True)
    lens_L3 = models.FloatField(blank = True, null = True)
    lens_2a = models.FloatField(blank = True, null = True)
    lens_2b = models.FloatField(blank = True, null = True)
    lens_2c = models.FloatField(blank = True, null = True)
    lens_L4 = models.FloatField(blank = True, null = True)
    lens_L5 = models.FloatField(blank = True, null = True)
    lens_D1 = models.FloatField(blank = True, null = True)
    lens_D2 = models.FloatField(blank = True, null = True)
    lens_Ua = models.FloatField(blank = True, null = True)
    lens_Ui = models.FloatField(blank = True, null = True)
    uhk_mitte = models.FloatField(verbose_name = 'UHK Mitte', blank = True, null = True)
    lens_3a = models.FloatField(blank = True, null = True)
    lens_3b = models.FloatField(blank = True, null = True)
    lens_3c = models.FloatField(blank = True, null = True)
    lens_A2 = models.FloatField(blank = True, null = True)
    lens_L6 = models.FloatField(blank = True, null = True)
    lens_L7 = models.FloatField(blank = True, null = True)
    lens_4a = models.FloatField(blank = True, null = True)
    lens_4b = models.FloatField(blank = True, null = True)
    lens_4c = models.FloatField(blank = True, null = True)
    lens_L8 = models.FloatField(blank = True, null = True)
    uex_mitte = models.FloatField(verbose_name = 'Uex Mitte', blank = True, null = True)
    lens_A3 = models.FloatField(default = 0, blank = True, null = True)
    lens_L10 = models.FloatField(default = 0, blank = True, null = True)
    lens_SK1 = models.FloatField(default = 0, blank = True, null = True)
    lens_SK2 = models.FloatField(default = 0, blank = True, null = True)
    nozzle = models.FloatField(verbose_name = 'Nozzle Temperature', default = 12, blank = True, null = True)
    qmh = models.CharField(max_length = 5, blank = True, verbose_name = 'QMH')
    comments = models.TextField(blank = True)

    def __unicode__(self):
        time = self.time.strftime('%d %m %Y, %H:%M')
        return u'%s: %s, %s' % (self.id, self.substance, time)

    def view_link(self):
        return "<a href='/wippi/view/%s/'>View</a>" % (self.id)

    view_link.allow_tags = True

    def file_link(self):
        return u'<a href=\'%s\'>File</a>' % (self.datafile.url)

    file_link.allow_tags = True

    class Meta:
        ordering = ['-time']

class Calibration(models.Model):
    time = models.DateTimeField(auto_now = False, auto_now_add = True)
    cal_base_file_1 = models.ForeignKey('Measurement', blank = True, null = True, related_name = 'calibration_cal_base_file', verbose_name = 'Basefile used for this cal.')
    formula = models.CharField(max_length=100, blank = True, verbose_name = 'Calibration formula for copy-pasting')
    logoutput = models.TextField(verbose_name = 'Log output of fitlib', blank = True)
    p0 = models.FloatField(blank = True)
    comments = models.TextField(blank = True)
    calibration_plot = models.FileField(upload_to = 'wippi/calibrations/', blank = True)    
    
    def __unicode__(self):
        return u'%s, %s' % (self.id, self.time)

    class Meta:
        ordering = ['-time']

class JournalEntry(models.Model):
    time = models.DateTimeField(auto_now = False, auto_now_add = False)
    operator = models.ForeignKey('Operator')
    comment = models.TextField()
    attachment = models.FileField(upload_to = 'wippi/techjournal/', blank = True, default = '')

    def __unicode__(self):
        return u'%s, %s, %s: %s' % (self.id, self.time, self.operator, self.comment[:50])

    class Meta:
        ordering = ['-time']
        verbose_name_plural = 'Journal Entries'
