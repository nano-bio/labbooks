import pytz
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils import http

from surftof.models import PotentialSettings, Measurement, Operator, Gas, Projectile, Surface, MeasurementType


class PotentialSettingsAdmin(admin.ModelAdmin):
    def proper_time(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d.%m.%Y, %H:%M')

    proper_time.short_description = 'Time and date'

    list_display = ('proper_time', 'id', 'get_short_description', 'estimated_impact_energy')
    list_filter = ()
    search_fields = ('comment', 'short_description', 'id',)
    readonly_fields = ('id',)
    ordering = ('-time',)
    actions = ['create_new_measurement_based_on_existing_one', ]

    fieldsets = (
        ('General', {
            'fields': (
                'id', 'time', 'short_description', 'estimated_impact_energy')}),
        ('Potentials source', {
            'fields': (
                ('spark_plug', 'nozzle'),
                'skimmer',)}),
        ('Potentials wien', {
            'fields': (
                ('wien_in', 'wien_out'),
                ('wien_e_top', 'wien_e_bottom'),
                'wien_magnet',)}),
        ('Potentials quadrupole', {
            'fields': (
                'focus_1', ('quad_ref', 'quad_field_axis'),)}),
        ('Potentials Surface', {
            'fields': (
                ('focus_2_inner', 'focus_2_outer'),
                'surface',
                ('focus_3_outer', 'focus_3_inner'),)}),
        ('Potentials ion space', {
            'fields': (
                'ion_spacer', 'extraction', 'focus_4', 'slit_disc',)}),
        ('Potentials TOF', {
            'fields': (
                ('tof_is_ref', 'tof_zero_level'),
                ('pusher', 'tof_drift_l1'),
                ('tof_l2', 'tof_ll'),
                'mcp')}),
        ('Stepper', {
            'fields': (
                ('surface_angle', 'slit_disc_angle'),
                ('stepper_surface_current_max', 'stepper_surface_current_standby'),
                ('stepper_slit_disc_current_max', 'stepper_slit_disc_current_standby')
            )
        }),
        ('TDC', {
            'fields': (
                ('tdc_extraction_time', 'tdc_frequency')
            )
        }),
        ('Comment', {
            'fields': (
                'comment',)})
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


class MeasurementsAdmin(admin.ModelAdmin):
    list_display = ('time', 'id', 'get_short_description', 'projectile', 'surface_material')
    list_filter = ('measurement_type', 'projectile', 'surface_material', 'gas_is', 'gas_surf')
    search_fields = ('comment', 'operator', 'projectile', 'surface_material', 'gas_is', 'gas_surf', 'id',)
    readonly_fields = ('id',)
    ordering = ('-time',)
    actions = ['create_new_measurement_based_on_existing_one', ]

    fieldsets = (
        ('General', {
            'fields': (
                'id',
                ('time', 'operator'),
                ('file_tof', 'file_surface_current'),
                'file_pressure_log',
                ('file_others', 'type_file_others'),
                'potential_settings',
                'measurement_type',
                'short_description',
                'rating')}),
        ('Chemical relevance', {
            'fields': (
                ('gas_is', 'gas_surf'), 'projectile',
                ('surface_material', 'surface_temperature'), 'tof_ions',
                'impact_energy',
                ('quadrupole_mass', 'quadrupole_resolution'))}),
        ('Pressures', {
            'fields': (
                ('pressure_ion_source_chamber', 'pressure_surface_chamber', 'pressure_tof_chamber')
            )}),
        ('Filaments', {
            'fields': (
                ('filament_source_voltage', 'filament_source_current'),
                ('filament_tof_voltage', 'filament_tof_current'),
                ('filament_tof_bottom_potential', 'filament_tof_bottom_current'),
            )
        }),
        ('Evaluation', {
            'fields': (
                ('file_evaluation', 'evaluated_by'),
                'evaluation_comment'
            )}),
        ('Comment', {'fields': ('comment',)})
    )

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        # we can only base it on one measurement
        if len(queryset) == 1:
            s = queryset.get()
            # this variable will hold all the values and is the address to the new setting form
            redirect_address = u'add/?'
            # we don't want these to be adopted
            forbidden_items = ['time', 'data_file_tof', 'data_file_surface']
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
admin.site.register(Measurement, MeasurementsAdmin)
admin.site.register(MeasurementType)
admin.site.register(Operator)
admin.site.register(Gas)
admin.site.register(Projectile)
admin.site.register(Surface)
