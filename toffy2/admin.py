from django.contrib import admin
import pytz

from labbooks.admin_common import create_new_entry_based_on_existing_one
from toffy2.models import Operator, Measurement


class MeasurementAdmin(admin.ModelAdmin):
    def proper_time(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d.%m.%Y, %H:%M')

    proper_time.short_description = 'Time and date'

    list_display = (
        'proper_time', 'id', 'operator', 'get_short_description', 'get_data_file', 'cluster_source_nozzle_temperature',
        'evaluated_by', 'evaporation_gas_bronkhorst_setpoint', 'collision_pressure', 'collision_energy')
    list_filter = ('operator',)
    search_fields = ('comment', 'data_file', 'short_description', 'id', 'evaporation_gas', 'collision_gas',
                     'oven_1_comment', 'oven_2_comment')
    readonly_fields = ('id',)
    save_as = True
    save_on_top = True
    ordering = ('-id',)

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
                'comment',
                ('evaluated_by', 'evaluation_file')
            )
        }),
        ('Pressures', {
            'fields': (
                'pressure_cs',
                'pressure_sector',
                'pressure_pu1',
                'pressure_pu2',
                'pressure_eva',
                'pressure_tof'
            )
        }),
        ('Cluster source', {
            'fields': (
                'cluster_source_he_pressure',
                'cluster_source_nozzle_temperature'
            )
        }),
        ('Ion source', {
            'fields': (
                'ion_source_ion_block_potential',
                'ion_source_electron_energy',
                'ion_source_electron_current',
                'ion_source_filament'
            )
        }),
        ('Sector', {
            'fields': (
                'sector_voltage_inner',
                'sector_voltage_outer'
            )
        }),
        ('Deflector', {
            'fields': (
                'deflector_1y',
                'deflector_1x',
                'deflector_2z',
                'deflector_2x',
                'deflector_plate'
            )
        }),
        ('Sample Gas', {
            'fields': (
                'sample_gas_bronkhorst_setpoint',
            )
        }),
        ('Oven 1', {
            'fields': (
                'oven_1_voltage',
                'oven_1_current',
                'oven_1_power',
                'oven_1_temperature',
                'oven_1_comment'
            )
        }),
        ('Oven 2', {
            'fields': (
                'oven_2_voltage',
                'oven_2_current',
                'oven_2_power',
                'oven_2_temperature',
                'oven_2_comment'
            )
        }),
        ('Evaporation gas', {
            'fields': (
                'evaporation_gas',
                'evaporation_gas_bronkhorst_setpoint'
            )
        }),
        ('Collision gas', {
            'fields': (
                'collision_gas',
                'collision_pressure',
                'collision_energy'
            )
        }),
    )

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        forbidden_items = ['time', '_state']
        return create_new_entry_based_on_existing_one(
            request,
            queryset,
            forbidden_items
        )


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Operator)
