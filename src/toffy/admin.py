import pytz
from django.contrib import admin

from labbooks.admin_common import create_new_entry_based_on_existing_one
from toffy.models import Operator, Measurement


class MeasurementAdmin(admin.ModelAdmin):
    def proper_time(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d.%m.%Y, %H:%M')

    proper_time.short_description = 'Time and date'

    list_display = (
        'proper_time', 'id', 'operator', 'get_short_description', 'get_data_file', 'nozzle_temperature',
        'electron_energy', 'electron_current', 'bender_float_voltage', 'oven_power', 'oven_temperature',
        'evaporation_pressure', 'collision_pressure', 'collision_energy', 'export_to_mscp')
    list_filter = ('operator',)
    search_fields = ('comment', 'data_file', 'short_description', 'id',)
    readonly_fields = ('id',)
    save_as = True
    save_on_top = True
    ordering = ('-time',)

    actions = ['create_new_measurement_based_on_existing_one', ]

    fieldsets = (
        ('General', {
            'fields': (
                'id',
                'time',
                'operator',
                'short_description',
                ('data_file', 'integration_start', 'integration_stop'),
                'tof_settings_file',
                'iseg_settings_file',
                'comment'
            )
        }),
        ('Cluster source', {
            'fields': (
                'he_pressure',
                'nozzle_temperature',
                'quad_pressure'

            )
        }),
        ('Ion source', {
            'fields': (
                'ion_block_potential',
                ('ion_source_deflector_vertical', 'ion_source_deflector_horizontal'),
                'electron_energy',
                'electron_current'
            )
        }),
        ('Quadrupole Bender', {
            'fields': (
                'bender_float_voltage',
                'bender_deflect_voltage'
            )
        }),
        ('Deflector', {
            'fields': (
                'deflector_float_z',
                'deflector_u_z',
                'deflector_float_y',
                'deflector_u_y',
                'deflector_front_aperture'
            )
        }),
        ('Oven', {
            'fields': (
                'oven_type',
                'oven_voltage',
                'oven_current',
                'oven_power',
                'oven_temperature',
                ('pickup_pressure', 'pickup_bronk')
            )
        }),
        ('Evaporation gas', {
            'fields': (
                'evaporation_gas',
                ('evaporation_pressure', 'evap_bronk')
            )
        }),
        ('Collision gas', {
            'fields': (
                'collision_gas',
                ('collision_pressure', 'coll_bronk'),
                'collision_energy'
            )
        }),
    )

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        forbidden_items = ['time', 'data_file']
        return create_new_entry_based_on_existing_one(
            request,
            queryset,
            forbidden_items
        )


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Operator)
