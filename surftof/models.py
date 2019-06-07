from django.db import models
from django.utils.timezone import now


class Operator(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return "{} {}.".format(self.firstname, self.lastname[0:1])


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
    slit_disc = models.FloatField(blank=True, null=True)
    tof_is_ref = models.FloatField(blank=True, null=True)
    pusher = models.FloatField(blank=True, null=True)
    tof_zero_level = models.FloatField(blank=True, null=True)
    tof_drift_l1 = models.FloatField(blank=True, null=True, verbose_name="TOF Drift and L1")
    tof_l2 = models.FloatField(blank=True, null=True, verbose_name="TOF L2")
    tof_ll = models.FloatField(blank=True, null=True, verbose_name="TOF LL")
    mcp = models.FloatField(blank=True, null=True, verbose_name="MCP")
    slit_disc_angle = models.FloatField(blank=True, null=True, verbose_name="Slit disc angle in degrees")
    surface_angle = models.FloatField(blank=True, null=True, verbose_name="Surface angle in degrees")

    # Additional comments
    comment = models.TextField(max_length=5000, blank=True)

    def get_short_description(self):
        return "{}...".format(self.short_description[:30])

    get_short_description.short_description = "SHORT DESCRIPTION"


ION_POLARITIES = (
    ('NEG', 'Negative'),
    ('POS', 'Positive'),
)


class Projectile(models.Model):
    name = models.CharField(max_length=50)
    polarity = models.CharField(max_length=3, choices=ION_POLARITIES, default='POS')

    def __str__(self):
        return "{} ({})".format(self.name, self.polarity)


class Gas(models.Model):
    name = models.CharField(max_length=100)
    chemical_formula = models.CharField(max_length=100)

    def __str__(self):
        return "{} ({})".format(self.name, self.chemical_formula)


class Surface(models.Model):
    name = models.CharField(max_length=100)
    chemical_formula = models.CharField(max_length=100, blank=True)
    comment = models.TextField(
        blank=True, max_length=5000,
        help_text="Additional information like purity, charge, serial number,...")

    def __str__(self):
        return "{} ({})".format(self.name, self.chemical_formula)


class Measurement(models.Model):
    # General
    time = models.DateTimeField(default=now)
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT, related_name="operator")
    file_tof = models.FileField(upload_to='surftof/dataFilesTof/', blank=True)
    file_surface_current = models.FileField(upload_to='surftof/dataFilesSurface/', blank=True)
    file_others = models.FileField(upload_to='surftof/dataFilesOthers/', blank=True)
    type_file_others = models.CharField(max_length=100, blank=True,
                                        help_text="Specify, what will be found in 'file others'")
    potential_settings = models.ForeignKey(PotentialSettings, on_delete=models.PROTECT, blank=True, null=True)

    # Chemical relevance
    gas_is = models.ForeignKey(Gas, on_delete=models.PROTECT, related_name="gas_is")
    gas_surf = models.ForeignKey(Gas, on_delete=models.PROTECT, related_name="gas_surf")
    projectile = models.ForeignKey(Projectile, on_delete=models.PROTECT, blank=True, null=True)
    surface_material = models.CharField(max_length=1500, blank=True)
    surface_temperature = models.FloatField(blank=True, null=True)
    tof_ions = models.CharField(max_length=3, choices=ION_POLARITIES, default='POS')
    impact_energy = models.FloatField(blank=True, null=True)
    quadrupole_mass = models.FloatField(blank=True, null=True)
    quadrupole_resolution = models.FloatField(blank=True, null=True)

    # Pressures
    pressure_ion_source_line = models.FloatField(blank=True, null=True)
    pressure_ion_source_chamber = models.FloatField(blank=True, null=True)
    pressure_surface_chamber = models.FloatField(blank=True, null=True)
    pressure_tof_chamber = models.FloatField(blank=True, null=True)

    # Filament ion source
    filament_voltage = models.FloatField(blank=True, null=True)
    filament_current = models.FloatField(blank=True, null=True)
    filament_bottom_potential = models.FloatField(blank=True, null=True)
    filament_bottom_current = models.FloatField(blank=True, null=True,
                                                help_text="The current is produced by the filament top")

    # Evaluation
    file_evaluation = models.FileField(upload_to='surftof/evaluation', blank=True)
    evaluated_by = models.ForeignKey(Operator, on_delete=models.PROTECT,
                                     related_name="evaluated_by", blank=True, null=True)
    evaluation_comment = models.TextField(blank=True, max_length=5000)

    # Comment
    comment = models.TextField(max_length=5000, blank=True)

    class Meta:
        ordering = ['-time']
        get_latest_by = 'time'
