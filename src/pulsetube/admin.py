from django.contrib import admin
from pulsetube import models


class MeasurementsAdmin(admin.ModelAdmin):
    list_display = (
        'date_time',
        'id',
        'operator',
        'get_comment',
        'he_temp',
        'ion_source_electron_energy',
        'ion_source_filament_current',
        'get_data_file',
        'scan_type'
    )
    list_filter = (
        'operator',
        'operator_2',
        'scan_type',
        'polarity'
    )
    search_fields = (
        'comment',
        'operator',
        'operator_2',
        'data_file',
        'scan_type',
        'id',
    )
    readonly_fields = ('id',)
    ordering = ('-id',)
    save_on_top = True

    fieldsets = (
        ('General', {
            'fields': (
                'id',
                'operator',
                'operator_2',
                'date_time',
                'data_file',
                'scan_type')}),
        ('Chamber Pressures', {
            'fields': (
                ('pressure_source', 'pressure_sector'),)}),
        ('He Source Settings', {
            'fields': (
                ('he_temp', 'he_pres'))}),
        ('Ion Source Settings', {
            'fields': (
                'ion_source_electron_energy',
                'ion_source_filament_current',
                'ion_source_fc_current')}),
        ('Sector Settings', {
            'fields': (
                'polarity',
                'channeltron_voltage',
                ('voltage_start', 'voltage_stop'),
                ('voltage_step_size', 'time_per_step'),
                'number_of_runs')}),
        ('Comment', {'fields': ('comment',)})
    )


# admin.site.register(models.Measurement, MeasurementsAdmin)
# admin.site.register(models.Person)
