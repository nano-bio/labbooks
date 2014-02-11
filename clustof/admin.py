from django.contrib import admin, messages
from clustof.models import Comment, Measurement, Operator, CurrentSetting, JournalEntry
from django.http import HttpResponseRedirect
from django.conf import settings

class CommentInline(admin.TabularInline):
    model = Comment

class MeasurementAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        return obj.time.strftime('%d %m %Y, %H:%M')
    propertime.short_description = 'Time and date'

    list_display = ('propertime', 'operator', 'scantype', 'substance', 'polarity', 'electron_energy', 'evaluated_by')
    list_filter = ('operator', 'time', 'scantype', 'polarity', 'evaluated_by')
    search_fields = ('substance', 'data_filename', 'tof_settings_file')
    save_as = True
    save_on_top = True
    ordering = ('-time',)

    inlines = [CommentInline]

    actions = ['create_new_measurement_based_on_existing_one', 'export_measurement']

    fieldsets = (
        ('General', {
            'fields': ('operator', 'data_filename', 'tof_settings_file', 'scantype', 'rating', 'time', 'evaluated_by', 'evaluation_file')
        }),
        ('Pressures', {
            'fields': ('pressure_cs', 'pressure_pu1', 'pressure_pu2', 'pressure_ion', 'pressure_tof'),
            'classes': ('wide',)
        }),
        ('CS settings', {
            'fields': ('temperature_he', 'stag_pressure_he', 'nozzle_diameter'),
            'classes': ('wide',)
        }),
        ('Voltages Ionsource', {
            'fields': ('electron_energy_set', 'real_electron_energy', 'ion_block', 'pusher', 'wehnelt', 'extraction_1', 'extraction_2', 'deflector_1', 'deflector_2', 'filament_current', 'trap_current', 'housing_current', 'faraday_cup', 'polarity'),
            'classes': ('wide',)
        }),
        ('Pickup', {
            'fields': ('oven_1_temperature', 'oven_1_power', 'oven_2_temperature', 'oven_2_power', 'substance'),
            'classes': ('wide',)
        }),
    )

    def export_measurement(self, request, queryset):
        #this is basically just a redirect
        if len(queryset) == 1:
            s = queryset.get()
            exporturl = '/clustof/export/files/' + s.data_filename.replace('D:\\Data\\','')
            return HttpResponseRedirect(exporturl)
        else:
            messages.error(request, 'You can only export ONE existing measurement, stupid.')

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        #we can only base it on one measurement
        if len(queryset) == 1:
            s = queryset.get()
            #this variable will hold all the values and is the address to the new measurement form
            redirect_address = 'add/?'
            #we don't want these to be adopted
            forbidden_items = ['_state', 'time', 'data_filename', 'rating']
            #walk through all fields of the model
            for item in s.__dict__:
                if item not in forbidden_items:
                    if s.__dict__[item] is not None:
                        redirect_address += item + '=' + str(s.__dict__[item]) + '&'

            #redirect to newly created address
            return HttpResponseRedirect(redirect_address)
        else:
            messages.error(request, 'You can only base a new measurement on ONE existing measurement, stupid.')

admin.site.register(Comment)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Operator)
admin.site.register(CurrentSetting)
admin.site.register(JournalEntry)
