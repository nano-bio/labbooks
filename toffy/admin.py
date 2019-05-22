from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils import http
import pytz

from toffy.models import Operator, Measurement


class MeasurementAdmin(admin.ModelAdmin):
    def proper_time(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d.%m.%Y, %H:%M')

    proper_time.short_description = 'Time and date'

    list_display = ('proper_time', 'id', 'operator', 'get_short_description', 'get_data_file',)
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
                'comment'
            )
        }),
        ('Cluster source', {
            'fields': (
                'he_pressure',
                'nozzle_temperature'

            )
        }),
        ('Ion source', {
            'fields': (
                'ion_block_potential',
                'electron_energy',
                'electron_current'
            )
        }),
        ('Quadrupole Bender', {
            'fields': (
                'bender_inner_voltage',
                'bender_outer_voltage'
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
                'oven_voltage',
                'oven_current',
                'oven_power',
                'oven_temperature'
            )
        }),
        ('Evaporation gas', {
            'fields': (
                'evaporation_gas',
                'evaporation_pressure'
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
        # we can only base it on one measurement
        if len(queryset) == 1:
            s = queryset.get()
            # this variable will hold all the values and is the address to the new measurement form
            redirect_address = u'add/?'
            # we don't want these to be adopted
            forbidden_items = ['time', 'data_file']
            # walk through all fields of the model
            for item in s.__dict__:
                if item not in forbidden_items:
                    if s.__dict__[item] is not None:
                        redirect_address += http.urlquote(item) + '=' + http.urlquote(s.__dict__[item]) + '&'

            # redirect to newly created address
            return HttpResponseRedirect(redirect_address)
        else:
            messages.error(request, 'You can only base a new measurement on ONE existing measurement, stupid.')


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Operator)
