import pytz
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils import http

from surftof.models import PotentialSettings, Operator


class PotentialSettingsAdmin(admin.ModelAdmin):
    def proper_time(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d.%m.%Y, %H:%M')

    proper_time.short_description = 'Time and date'

    list_display = ('proper_time', 'id', 'get_short_description')
    list_filter = ('potential_type',)
    search_fields = ('comment', 'short_description', 'id',)
    readonly_fields = ('id',)
    ordering = ('-time',)

    actions = ['create_new_measurement_based_on_existing_one', ]

    fieldsets = (
        ('General', {
            'fields': (
                'id',
                'time',
                'short_description',
                'potential_type')}),
        ('Potentials', {
            'fields': (
                ('spark_plug', 'nozzle'), 'skimmer', ('wien_in', 'wien_out'), ('wien_e_top', 'wien_e_bottom'),
                'wien_magnet', 'focus_1', ('quad_ref', 'quad_field_axis'), ('focus_2_inner', 'focus_2_outer'),
                'surface', ('focus_3_outer', 'focus_3_inner'), 'ion_spacer', 'extraction', 'focus_4', 'slit_disc',
                'tof_is_ref', 'pusher', 'tof_zero_level', ('tof_drift_l1', 'tof_l2', 'tof_ll'), 'mcp')}),
        ('Comment', {'fields': ('comment',)})
    )

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        # we can only base it on one measurement
        if len(queryset) == 1:
            s = queryset.get()
            # this variable will hold all the values and is the address to the new setting form
            redirect_address = u'add/?'
            # we don't want these to be adopted
            forbidden_items = ['time', ]
            # walk through all fields of the model
            for item in s.__dict__:
                if item not in forbidden_items:
                    if s.__dict__[item] is not None:
                        redirect_address += http.urlquote(item) + '=' + http.urlquote(s.__dict__[item]) + '&'

            # redirect to newly created address
            return HttpResponseRedirect(redirect_address)
        else:
            messages.error(request, 'You can only base a new potential setting on ONE existing setting, stupid.')


admin.site.register(PotentialSettings, PotentialSettingsAdmin)
admin.site.register(Operator)
