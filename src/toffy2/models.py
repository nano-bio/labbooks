from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from journal.models import BasicJournalEntry


class Operator(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Measurement(models.Model):
    time = models.DateTimeField(default=now)
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT, related_name='operator')
    short_description = models.CharField(max_length=500, blank=True)
    rating = models.IntegerField(choices=((1, 'good'), (2, 'neutral'), (3, 'bad')), default=2)
    integration_start = models.IntegerField(blank=True, null=True, verbose_name="Integration start [s]")
    integration_stop = models.IntegerField(blank=True, null=True, verbose_name="Integration stop [s]")
    data_file_path_h5 = models.CharField(
        max_length=150, blank=True,
        help_text="The path must start with Z:\\, otherwise spectra viewer won't work!",
        default="Z:\\Experiments\\Toffy2\\Measurements\\RAW-TOFWERK-Data\\", )
    data_file = models.FileField(upload_to='toffy2/dataFiles/', blank=True,
                                 help_text="Export massspecs and upload plain text files only.")
    tof_settings_file = models.FileField(upload_to='toffy2/settingsFiles/', blank=True,
                                         verbose_name="TOF settings file")
    comment = models.TextField(max_length=5000, blank=True)
    evaluated_by = models.ForeignKey(Operator, on_delete=models.PROTECT, related_name='evaluated_by', blank=True,
                                     null=True)
    evaluation_file = models.FileField(upload_to='toffy2/evaluationFiles/', blank=True)

    pressure_cs = models.FloatField(verbose_name="Pressure CS [mbar]")
    pressure_sector = models.FloatField(verbose_name="Pressure Sector [mbar]")
    pressure_pu1 = models.FloatField(verbose_name="Pressure PU1 [mbar]", blank=True, null=True)
    pressure_pu2 = models.FloatField(verbose_name="Pressure PU2 [mbar]", blank=True, null=True)
    pressure_eva = models.FloatField(verbose_name="Pressure EVA [mbar]")
    pressure_tof = models.FloatField(verbose_name="Pressure TOF [mbar]")

    cluster_source_he_pressure = models.FloatField(verbose_name="He pressure [bar]")
    cluster_source_nozzle_temperature = models.FloatField(verbose_name="Nozzle temperature [K]")

    ion_source_ion_block_potential = models.FloatField(verbose_name="Ion block potential [V]")
    ion_source_electron_energy = models.FloatField(verbose_name="Electron energy [eV]")
    ion_source_electron_current = models.FloatField(verbose_name="Electron current [uA]")
    ion_source_filament = models.FloatField(verbose_name="Filament [A]")

    sector_voltage_inner = models.FloatField(verbose_name="Inner sector [V]")
    sector_voltage_outer = models.FloatField(verbose_name="Outer sector [V]")

    deflector_1y = models.FloatField(verbose_name="Defl 1Y [V]")
    deflector_1x = models.FloatField(verbose_name="Defl 1X [V]")
    deflector_2z = models.FloatField(verbose_name="Defl 2Z [V]")
    deflector_2x = models.FloatField(verbose_name="Defl 2X [V]")
    deflector_plate = models.FloatField(verbose_name="Plate [V]")

    sample_gas_bronkhorst_setpoint = models.FloatField(verbose_name="Bronkhorst Setpoint [%]")

    oven_1_voltage = models.FloatField(verbose_name="Voltage [V]", blank=True, null=True)
    oven_1_current = models.FloatField(verbose_name="Current [I]", blank=True, null=True)
    oven_1_power = models.FloatField(verbose_name="Power [W]", blank=True, null=True)
    oven_1_temperature = models.FloatField(verbose_name="Temperature [C]", blank=True, null=True)
    oven_1_comment = models.TextField(verbose_name="Comment", blank=True, max_length=5000)

    oven_2_voltage = models.FloatField(verbose_name="Voltage [V]", blank=True, null=True)
    oven_2_current = models.FloatField(verbose_name="Current [I]", blank=True, null=True)
    oven_2_power = models.FloatField(verbose_name="Power [W]", blank=True, null=True)
    oven_2_temperature = models.FloatField(verbose_name="Temperature [C]", blank=True, null=True)
    oven_2_comment = models.TextField(verbose_name="Comment", blank=True, max_length=5000)

    evaporation_gas = models.CharField(verbose_name="Gas", max_length=100, default="Helium")
    evaporation_gas_bronkhorst_setpoint = models.FloatField(verbose_name="Bronkhorst Setpoint [%]", null=True,
                                                            blank=True)

    collision_gas = models.CharField(verbose_name="Gas", max_length=100, blank=True, null=True)
    collision_pressure = models.FloatField(verbose_name="Pressure [mbar]", blank=True, null=True)
    collision_energy = models.FloatField(verbose_name="Energy [eV]", blank=True, null=True)

    # this provides a link to the data file in the admin interface
    def get_data_file(self):
        if self.data_file:
            return mark_safe(f"<a href='/files/{self.data_file}' download>Data file</a>")
        return ""

    def get_short_description(self):
        if len(self.short_description) > 35:
            return f"{self.short_description[:30]}..."
        return self.short_description

    def rating_buttons(self):
        return mark_safe(f"""<div
            id='rating-container-{self.id}'
            style='white-space: nowrap; cursor: pointer;'
            class='thumb'
            data-id='{self.id}'
            data-rating='{self.rating}'
            ></div>""")

    rating_buttons.short_description = ''

    def export_to_mscp(self):
        return mark_safe(
            f"<a href='{reverse('mscp-start-from-admin-measurements', args=('toffy2', self.pk))}'>MSCP-Upload</a>")

    def __str__(self):
        return f"{self.time}, {self.operator}"

    class Meta:
        ordering = ['-time']
        get_latest_by = 'time'


class JournalEntry(BasicJournalEntry):
    pass
