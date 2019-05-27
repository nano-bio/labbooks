from django.db import models
from django.utils.timezone import now


class Operator(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)


POTENTIAL_TYPES = (
    ('RG', 'Residual gas'),
    ('SURF', 'Up to surface only'),
    ('ALL', 'All'),
    ('ELSE', 'Else. See description / comment')
)


class PotentialSettings(models.Model):
    # General
    time = models.DateTimeField(default=now)
    potential_type = models.CharField(max_length=4, choices=POTENTIAL_TYPES, default='ALL')
    short_description = models.CharField(max_length=500, blank=True)

    # Ion lens potentials
    spark_plug = models.FloatField(blank=True, null=True)
    nozzle = models.FloatField(blank=True, null=True)
    skimmer = models.FloatField(blank=True, null=True)
    wien_in = models.FloatField(blank=True, null=True)
    wien_out = models.FloatField(blank=True, null=True)
    wien_e_top = models.FloatField(blank=True, null=True)
    wien_e_bottom = models.FloatField(blank=True, null=True)
    wien_magnet = models.FloatField(blank=True, null=True)
    focus_1 = models.FloatField(blank=True, null=True)
    quad_ref = models.FloatField(blank=True, null=True)
    quad_field_axis = models.FloatField(blank=True, null=True)
    focus_2_inner = models.FloatField(blank=True, null=True)
    focus_2_outer = models.FloatField(blank=True, null=True)
    surface = models.FloatField(blank=True, null=True)
    focus_3_outer = models.FloatField(blank=True, null=True)
    focus_3_inner = models.FloatField(blank=True, null=True)
    ion_spacer = models.FloatField(blank=True, null=True)
    extraction = models.FloatField(blank=True, null=True)
    focus_4 = models.FloatField(blank=True, null=True)
    tof_is_ref = models.FloatField(blank=True, null=True)
    pusher = models.FloatField(blank=True, null=True)
    tof_zero_level = models.FloatField(blank=True, null=True)
    tof_drift_l1 = models.FloatField(blank=True, null=True, verbose_name="TOF Drift and L1")
    tof_l2 = models.FloatField(blank=True, null=True, verbose_name="TOF L2")
    tof_ll = models.FloatField(blank=True, null=True, verbose_name="TOF LL")
    mcp = models.FloatField(blank=True, null=True, verbose_name="MCP")

    # Additional comments
    comment = models.TextField(max_length=5000, blank=True)

    def get_short_description(self):
        return "{}...".format(self.short_description[:30])


"""
POLARITIES = (
    ('NEG', 'Negative'),
    ('POS', 'Positive'),
)

class Projectile(models.Model):
    name = models.CharField(max_length=50)
    polarity = models.CharField(max_length=3, choices=POLARITIES, default='POS')
    comment = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    # General
    time = models.DateTimeField(default=now)
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT)
    data_file = models.FileField(upload_to='surftof/dataFiles/')
    settings_potentials = models.ForeignKey(Settings, on_delete=models.PROTECT)
    surface_temperature = models.FloatField(blank=True, null=True)
    surface_material = models.CharField(max_length=1500, blank=True)

    gas_is = models.CharField(verbose_name="Gas IS", max_length=500, blank=True)
    gas_surf = models.CharField(verbose_name="Gas Surface", max_length=500, blank=True)
    projectile = models.ForeignKey(Projectile, on_delete=models.PROTECT)

    # Pressures
    pressure_ion_source_line = models.FloatField(blank=True, null=True)
    pressure_ion_source_chamber = models.FloatField(blank=True, null=True)
    pressure_surface_chamber = models.FloatField(blank=True, null=True)
    pressure_tof = models.FloatField(blank=True, null=True)

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
"""
