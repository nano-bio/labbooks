from django.db import models

ENERGYSCAN = 'ES'
MASSSCAN = 'MS'
MIKESCAN = 'MIKE'

SCANTYPES = (
    (ENERGYSCAN, 'Energyscan'),
    (MASSSCAN, 'Massscan'),
    (MIKESCAN, 'MIKE-Scan'),
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
    datafile = models.FileField(upload_to = 'vg/%Y/%m/%d/%H/%M/%S/')
    scantype = models.CharField(max_length = 20, choices = SCANTYPES, default = ENERGYSCAN)
    electron_energy = models.FloatField(blank = True, null = True, verbose_name = 'Electron Energy (for MS)')
    substance = models.CharField(max_length = 100)
    description = models.CharField(max_length = 200)
    channeltron = models.FloatField(default = 2.3, verbose_name = 'Channeltron (kV)')
    ionblock_temperature = models.PositiveIntegerField(default = 160)
    trap_current = models.PositiveIntegerField(default = 50)
    filament_current = models.FloatField()
    pressure_ionblock = models.CharField(max_length = 7, default = '1e-6', verbose_name = 'Pressure Ion Block (mbar)')
    pressure_analyzer = models.CharField(max_length = 7, default = '1e-8', verbose_name = 'Pressure Analyzer (mbar)')
    background_pressure = models.FloatField(blank = True, null = True, verbose_name = 'Background Pressure in IS (mbar)')
    ion_repeller = models.FloatField(default = 5.7)
    focus_coarse_1 = models.PositiveIntegerField()
    focus_coarse_2 = models.PositiveIntegerField()
    focus_fine_1 = models.FloatField(default = 5.0)
    focus_fine_2 = models.FloatField(default = 5.0)
    deflector_1 = models.FloatField()
    deflector_2 = models.FloatField()
    ion_energy = models.FloatField()
    y_focus = models.FloatField(verbose_name='Y-Focus')
    x_deflect = models.FloatField(verbose_name='Y-Deflect')
    z_deflect = models.FloatField(verbose_name='Z-Deflect')
    curve_1 = models.FloatField()
    rotate_1 = models.FloatField()
    z_deflect_1 = models.FloatField(verbose_name='Z-Deflect 1')
    z_focus_1 = models.FloatField(verbose_name='Z-Focus 1')
    curve_2 = models.FloatField()
    rotate_2 = models.FloatField()
    z_deflect_2 = models.FloatField(verbose_name='Z-Deflect 2')
    z_focus_2 = models.FloatField(verbose_name='Z-Focus 2')
    comments = models.TextField()

    def __unicode__(self):
        time = self.time.strftime('%d %m %Y, %H:%M')
        return u'%s: %s, %s' % (self.id, self.substance, time)

    class Meta:
        ordering = ['-time']

class Calibration(models.Model):
    time = models.DateTimeField(auto_now = False, auto_now_add = True)
    cal_base_file_1 = models.ForeignKey('Measurement', blank = True, null = True, related_name = 'calibration_cal_base_file_1', verbose_name = 'Basefile 1 used for this cal.')
    cal_base_file_2 = models.ForeignKey('Measurement', blank = True, null = True, related_name = 'calibration_cal_base_file_2', verbose_name = 'Basefile 2 used for this cal.')
    cal_base_file_3 = models.ForeignKey('Measurement', blank = True, null = True, related_name = 'calibration_cal_base_file_3', verbose_name = 'Basefile 3 used for this cal.')
    cal_base_file_4 = models.ForeignKey('Measurement', blank = True, null = True, related_name = 'calibration_cal_base_file_4', verbose_name = 'Basefile 4 used for this cal.')
    formula = models.CharField(max_length=100, blank = True, verbose_name = 'Calibration formula for copy-pasting')
    logoutput = models.TextField(verbose_name = 'Log output of fitlib', blank = True)
    p0 = models.FloatField(blank = True)
    p1 = models.FloatField(blank = True)
    p2 = models.FloatField(blank = True)
    comments = models.TextField(blank = True)
    calibration_plot = models.FileField(upload_to = 'vg/calibrations/', blank = True)    
    
    def __unicode__(self):
        if self.p2 is '':
            quadratic = 'No'
        else:
            quadratic = 'Yes'
        return u'%s, %s, Quadratic: %s' % (self.id, self.time, quadratic)

class JournalEntry(models.Model):
    time = models.DateTimeField(auto_now = False, auto_now_add = True)
    operator = models.ForeignKey('Operator')
    comment = models.TextField()
