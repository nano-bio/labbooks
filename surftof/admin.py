import pytz
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils import http

from surftof.models import PotentialSettings, Measurement


class PotentialSettingsAdmin(admin.ModelAdmin):
    def proper_time(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d.%m.%Y, %H:%M')

    proper_time.short_description = 'Time and date'

    list_display = ('proper_time', 'id', 'get_short_description', 'potential_type')
    list_filter = ('potential_type',)
    search_fields = ('comment', 'short_description', 'id',)
    readonly_fields = ('id',)
    ordering = ('-time',)
    actions = ['create_new_measurement_based_on_existing_one', ]

    fieldsets = (
        ('General', {
            'fields': (
                'id', 'time', 'short_description', 'potential_type')}),
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
                ('surface_angle', 'slit_disc_angle')
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

    def title(self, obj):
        return '{}: {} on {} ...'.format(
            obj.time.strftime('%d.%m.%Y, %H:%M'), obj.projectile[0:10], obj.surface_material[0:80])

    title.short_description = 'Date, time'
    list_display = ('title', 'id', 'operator', 'projectile', 'surface_material')
    list_filter = ('operator', 'projectile', 'surface_material', 'gas_is', 'gas_surf')
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
                ('file_others', 'type_file_others'),
                'potential_settings')}),
        ('Chemical relevance', {
            'fields': (
                ('gas_is', 'gas_surf'), 'projectile',
                ('surface_material', 'surface_temperature'), 'tof_ions',
                'impact_energy',
                ('quadrupole_mass', 'quadrupole_resolution'))}),
        ('Pressures', {
            'fields': (
                ('pressure_ion_source_line', 'pressure_ion_source_chamber'),
                ('pressure_surface_chamber', 'pressure_tof_chamber')
            )}),
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
