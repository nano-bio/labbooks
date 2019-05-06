from django.db import models


class Operator(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)


class Measurement(models.Model):
    time = models.DateTimeField()
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT)
    short_description = models.CharField(max_length=500, blank=True)
    integration_start = models.IntegerField(blank=True, null=True, verbose_name="Integration start [s]")
    integration_stop = models.IntegerField(blank=True, null=True, verbose_name="Integration stop [s]")
    data_file = models.FileField(upload_to='toffy/dataFiles/', blank=True,
                                 help_text="Export massspecs and upload plain text files only.")
    tof_settings_file = models.FileField(upload_to='toffy/settingsFiles/', blank=True, verbose_name="TOF settings file")
    comment = models.TextField(max_length=5000, blank=True)

    he_pressure = models.FloatField(verbose_name="He pressure [bar]", default=20, blank=True, null=True)
    nozzle_temperature = models.FloatField(verbose_name="Nozzle temperature [K]", blank=True, null=True)

    ion_block_potential = models.FloatField(verbose_name="Ion block potential [V]", blank=True, null=True)
    electron_energy = models.FloatField(verbose_name="Electron energy [eV]", blank=True, null=True)
    electron_current = models.FloatField(verbose_name="Electron current [uA]", blank=True, null=True)

    bender_inner_voltage = models.FloatField(verbose_name="Inner voltage [V]", blank=True, null=True)
    bender_outer_voltage = models.FloatField(verbose_name="Outer voltage [V]", blank=True, null=True)

    deflector_float_z = models.FloatField(verbose_name="Float Z [V]", blank=True, null=True)
    deflector_u_z = models.FloatField(verbose_name="U Z [V]", blank=True, null=True)
    deflector_float_y = models.FloatField(verbose_name="Float Y [V]", blank=True, null=True)
    deflector_u_y = models.FloatField(verbose_name="U Y [V]", blank=True, null=True)
    deflector_front_aperture = models.FloatField(verbose_name="Front aperture [V]", blank=True, null=True)

    oven_voltage = models.FloatField(verbose_name="Voltage [V]", blank=True, null=True)
    oven_current = models.FloatField(verbose_name="Current [I]", blank=True, null=True)
    oven_power = models.FloatField(verbose_name="Power [W]", blank=True, null=True)
    oven_temperature = models.FloatField(verbose_name="Temperature [°C]", blank=True, null=True)

    evaporation_gas = models.FloatField(verbose_name="Gas", blank=True, null=True, default="Helium")
    evaporation_pressure = models.FloatField(verbose_name="Pressure [mbar]", blank=True, null=True)

    collision_gas = models.FloatField(verbose_name="Gas", blank=True, null=True, default="Argon")
    collision_pressure = models.FloatField(verbose_name="Pressure [mbar]", blank=True, null=True)
    collision_energy = models.FloatField(verbose_name="Energy [eV]", blank=True, null=True)

    # this provides a link to the data file in the admin interface
    def get_data_file(self):
        return "<a href='%s'>Data file</a>" % ('/toffy/dataFiles/' + str(self.data_file))

    get_data_file.allow_tags = True

    def get_short_description(self):
        return "{}...".format(self.short_description[:30])

    def __unicode__(self):
        return u'%s, %s' % (self.time, self.operator)

    class Meta:
        ordering = ['-time']
        get_latest_by = 'time'
