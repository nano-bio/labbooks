import pytz
from django.contrib import admin
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from labbooks.admin_common import create_new_entry_based_on_existing_one, create_new_entry_based_on_existing_one_url
from surftof.models import PotentialSettings, Measurement, Gas, Surface, MeasurementType, JournalEntry


class PotentialSettingsAdmin(admin.ModelAdmin):
    def proper_time(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d.%m.%Y, %H:%M')

    proper_time.short_description = 'Time and date'

    list_display = ('proper_time', 'id', 'get_short_description', 'get_impact_energy')
    list_filter = ()
    search_fields = ('comment', 'short_description', 'id',)
    readonly_fields = ('id',)
    ordering = ('-time',)
    actions = ['create_new_measurement_based_on_existing_one', ]

    fieldsets = (
        ('General', {
            'fields': (
                'id', 'time', 'short_description')}),
        ('Potentials source', {
            'fields': (
                ('source_pusher', 'source_ion_spacer'),
                ('focus_1a', 'focus_1b'),
                'source_cage')}),
        ('Potentials quadrupole', {
            'fields': (
                ('quad_ref', 'quad_field_axis'),)}),
        ('Potentials Surface', {
            'fields': (
                ('focus_2_inner', 'focus_2_outer'),
                'surface',
                ('focus_3_outer', 'focus_3_inner'),)}),
        ('Potentials ion space', {
            'fields': (
                ('ion_spacer', 'extraction'),
                ('focus_4', 'slit_disc'),
                'tof_is_ref',)}),
        ('Potentials TOF', {
            'fields': (
                ('tof_zero_level', 'pusher'),
                'tof_drift_l1',
                ('tof_l2', 'tof_ll'),
                'mcp')}),
        ('Stepper', {
            'fields': (
                ('surface_angle', 'slit_disc_angle'),
                ('stepper_surface_current_max', 'stepper_surface_current_standby'),
                ('stepper_slit_disc_current_max', 'stepper_slit_disc_current_standby')
            )
        }),
        ('Filaments', {
            'fields': (
                ('filament_source_voltage', 'filament_source_current'),
                ('filament_tof_voltage', 'filament_tof_current'),
                ('filament_tof_bottom_potential', 'filament_tof_bottom_current'),
            )
        }),
        ('Comment', {
            'fields': (
                'comment',)})
    )

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        forbidden_items = ['time', '_state']
        return create_new_entry_based_on_existing_one(
            request,
            queryset,
            forbidden_items
        )


class MeasurementsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'create_new_measurement_based_on_existing_one_inline', 'get_short_description', 'projectile',
        'get_surface', 'get_impact_energy_surface', 'get_surface_temperature', 'gas_surf', 'get_rating_stars')
    list_filter = ('measurement_type', 'projectile', 'surface_material', 'gas_is', 'gas_surf')
    search_fields = ('comment', 'projectile', 'surface_material__name', 'gas_is__name', 'gas_surf__name', 'id',
                     'short_description')
    readonly_fields = ('id',)
    actions = ['create_new_measurement_based_on_existing_one', ]
    save_on_top = True

    fieldsets = (
        ('General', {
            'fields': (
                'id',
                'time',
                'potential_settings',
                'measurement_type',
                'short_description',
                'rating')}),
        ('Chemical relevance', {
            'fields': (
                ('gas_is', 'gas_surf'),
                ('gas_setpoint_is', 'gas_setpoint_surf'),
                'projectile',
                ('surface_material', 'surface_temperature'), 'tof_ions',
                ('quadrupole_mass', 'quadrupole_resolution'))}),
        ('Impact energies', {
            'fields': (
                ('electron_impact_energy_source', 'electron_impact_energy_source_current'),
                ('electron_impact_energy_tof', 'electron_impact_energy_tof_current'))}),
        ('Filaments', {
            'fields': (
                ('filament_is_voltage', 'filament_is_current'),
                ('filament_tof_voltage', 'filament_tof_current'))}),
        ('Comment', {'fields': ('comment',)})
    )

    def create_new_measurement_based_on_existing_one_inline(self, s):
        forbidden_items = ['time', '_state']
        url = create_new_entry_based_on_existing_one_url(s, forbidden_items)
        return mark_safe(
            f"<a href='{url}' title='Duplicate this measurement'>"
            f"<img src='{static('images/clipboard-plus.svg')}'>"
            f"</a>")

    create_new_measurement_based_on_existing_one_inline.short_description = ""


admin.site.register(PotentialSettings, PotentialSettingsAdmin)
admin.site.register(Measurement, MeasurementsAdmin)
admin.site.register(MeasurementType)
admin.site.register(Gas)
admin.site.register(Surface)
admin.site.register(JournalEntry)
