from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import time, datetime
from django.core.exceptions import ValidationError
from django.conf import settings

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
    time = models.DateTimeField(auto_now = False, auto_now_add = False)
    data_filename = models.CharField(max_length=1500, verbose_name = 'Filename', default = 'D:\\Data\\')
    operator = models.ForeignKey('Operator')
    pressure_is = models.FloatField(verbose_name = 'Pressure IS', default = float('4e-5'))
    pressure_surface = models.FloatField(verbose_name = 'Pressure Surface', default = float('3e-6'))
    pressure_cube = models.FloatField(verbose_name = 'Pressure Cube', default = float('1e-6'))
    pressure_tof = models.FloatField(verbose_name = 'Pressure TOF', default = float('3e-7'))
    u_surf = models.FloatField(blank = True, null = True, verbose_name = 'Surface Potential')
    u_is = models.FloatField(blank = True, null = True, verbose_name = 'IS/Quad Potential')
    surface_current = models.FloatField(blank = True, null = True)
    surface_temperature = models.FloatField(blank = True, null = True)
    heating_current = models.FloatField(blank = True, null = True)
    surface_material = models.TextField(max_length=1500)
    projectile = models.TextField(max_length=1500)
    polarity = models.CharField(max_length = 3, choices = POLARITIES, default = 'NEG')
    evaluated_by = models.CharField(max_length = 20, blank = True)
    evaluation_file = models.FileField(upload_to = 'surftof/evaluations/', blank = True, default = '')
    fil_cur = models.FloatField(verbose_name = 'Filament Current', blank = True, null = True)
    fil_vol = models.FloatField(verbose_name = 'Filament Voltage', blank = True, null = True)
    far_cup = models.FloatField(verbose_name = 'Trap Current', blank = True, null = True)
    pusher_is = models.FloatField(verbose_name = 'Pusher IS',  blank = True, null = True)
    ion_block = models.FloatField(verbose_name = 'Ion Block', blank = True, null = True)
    zb1r = models.FloatField(verbose_name = 'ZB1 R', blank = True, null = True)
    zb1l = models.FloatField(verbose_name = 'ZB1 L', blank = True, null = True)
    zb_2 = models.FloatField(verbose_name = 'ZB2', blank = True, null = True)
    zyl1r = models.FloatField(verbose_name = 'Zyl1 R', blank = True, null = True)
    zyl1l = models.FloatField(verbose_name = 'Zyl1 L', blank = True, null = True)
    zyl2 = models.FloatField(verbose_name = 'Zyl 2', blank = True, null = True)
    def_ou = models.FloatField(verbose_name = 'Def O/U', blank = True, null = True)
    def_r = models.FloatField(verbose_name = 'Def R', blank = True, null = True)
    def_l = models.FloatField(verbose_name = 'Def L', blank = True, null = True)
    is_plate = models.FloatField(verbose_name = 'IS front Plate', blank = True, null = True)
    pusher_tof = models.FloatField(verbose_name = 'Pusher Tof', blank = True, null = True, default = 400)
    zl_grid = models.FloatField(verbose_name = 'Zero Level Grid', blank = True, null = True, default = 0)
    acc_grid = models.FloatField(verbose_name = 'Acceleration Grid', blank = True, null = True, default = -2000)
    def_r_tof = models.FloatField(verbose_name = 'Deflector R Tof', blank = True, null = True, default = -2000)
    def_l_tof = models.FloatField(verbose_name = 'Deflector L Tof', blank = True, null = True, default = -2000)
    drift = models.FloatField(verbose_name = 'Drift Tube', blank = True, null = True, default = -2000)
    reflectron = models.FloatField(verbose_name = 'Reflectron', blank = True, null = True, default = 2000)
    post_acc = models.FloatField(verbose_name = 'Post Accelaration', blank = True, null = True, default = - 4800)
    mcp = models.FloatField(verbose_name = 'MCP', blank = True, null = True, default = 2300)

    # this provides a link to the eval file in the admin interface

    def eval_file(self):
        if self.evaluation_file:
            return "<a href='%s'>Eval. file</a>" % (self.evaluation_file.url)
        else:
            return ''

    eval_file.allow_tags = True

    # same for the actual data file

    def data_file(self):
        return "<a href='%s'>Data file</a>" % ('/surftof/export/' + str(self.id))

    data_file.allow_tags = True

    def __unicode__(self):
        return u'%s, %s: %s on %s ...' % (self.time, self.operator, self.projectile[0:10], self.surface_material[0:80])

    def collision_energy(self):
        ee = self.u_is - self.u_surf
        return ee

    def clean(self):
        # cleaning method. first thing, check if file extension is there
        try:
            fn = self.data_filename.split('\\')[2]
        except IndexError:
            raise ValidationError('Something is odd about this filename. Did you forget the path?')

    class Meta:
        ordering = ['-time']
        get_latest_by = 'time'

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

    class Meta:
        verbose_name_plural = "Vacuum Status"

    def __unicode__(self):
        return u'Pressures at %s' % (datetime.datetime.fromtimestamp(self.time).strftime('%c')) 
