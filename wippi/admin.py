from wippi.models import *
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files import File
from django.db.models.fields.files import FieldFile
from django.utils import http
from django.contrib.admin.sites import AdminSite

import sys
import pytz
sys.path.append('/var/opt/')

import fitlib

class MeasurementAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d %m %Y, %H:%M')
    propertime.short_description = 'Time and date'

    list_display = ('propertime', 'substance', 'fragment', 'description', 'scantype', 'file_link', 'view_link')
    list_filter = ('operator', 'time', 'scantype')
    search_fields = ('substance', 'description')
    save_as = True
    save_on_top = True
    ordering = ('-time',)

    actions = ['create_new_calibration', 'create_new_measurement_based_on_existing_one']

    fieldsets = (
        ('General', {
            'fields': ('operator', 'datafile', 'scantype', 'polarity', 'substance', 'substance_comment', 'fragment', 'description', 'time')
        }),
        ('Pressures', {
            'fields': ('pressure_monochromator', 'pressure_pickup', 'base_pressure', 'pressure_cs', 'background_pressure'),
            'classes': ('wide',)
        }),
        ('Quadrupole Lenses', {
            'fields': ('ion_energy', 'optics_inside', 'optics_outside', 'def_a', 'def_i', 'field_axis'),
            'classes': ('wide',)
        }),
        ('WIPPI settings', {
            'fields': ('qmh', 'channeltron_1', 'channeltron_2', 'oven_temperature', 'chamber_temperature', 'faraday_current', 'filament_current', 'electron_energy', 'emission', 'energy_resolution', 'mass_resolution', 'nozzle'),
            'classes': ('wide',)
        }),
        ('Lenses', {
            'fields': ('anode', 'coil_voltage_xy', 'coil_voltage_xz', 'coil_voltage_yz', 'coil_current_xy', 'coil_current_xz', 'coil_current_yz', 'lens_1a', 'lens_1b', 'lens_1c', 'lens_A1', 'lens_L2', 'lens_L3', 'lens_2a', 'lens_2b', 'lens_2c', 'lens_L4', 'lens_L5', 'lens_D1', 'lens_D2', 'lens_Ua', 'lens_Ui', 'uhk_mitte', 'lens_3a', 'lens_3b', 'lens_3c', 'lens_A2', 'lens_L6', 'lens_L7', 'lens_4a', 'lens_4b', 'lens_4c', 'lens_L8', 'uex_mitte', 'lens_A3', 'lens_L10', 'lens_SK1', 'lens_SK2', 'ue', 'ue_fine'),
            'classes': ('wide',)
        }),
        ('Comments', {
            'fields': ('comments',),
            'classes': ('wide',)
        })
    )

    def create_new_calibration(self, request, queryset):
        if len(queryset) > 1:
            messages.error(request, 'Choose only 1 measurement to create a new calibration')
        else:
            #let's set up an empty calibration right away and save it, so we can get the id. we need that to save the file
            new_cal = Calibration(p0 = 0)
            new_cal.save()

            cal_measurement = queryset.get()

            #first we get all the corresponding filenames and measurement_IDs to the measurements selected
            cal_filename = settings.MEDIA_ROOT + cal_measurement.datafile.name
            file_id = cal_measurement.id

            #create a unique filename
            filename = settings.MEDIA_ROOT + 'wippi/calibrations/' + str(new_cal.id) + '.pdf'

            #actually try some fitting
            parameter, log = fitlib.SF6_calibration.do_CCl4_calibration(cal_filename, showplots = False, outputfile = filename)

            #create a FieldFile object
            f = open(filename)
            new_cal.calibration_plot.save(filename, File(f))

            #create an easily copy-pastable formula
            formula = 'y = x + %s' % (parameter)

            #fill our new calibration with the values retrieved from fitlib
            new_cal.logoutput = log
            new_cal.p0 = parameter
            new_cal.formula = formula
            new_cal.cal_base_file_1 = Measurement.objects.get(id = file_id)

            #last but not least: save it
            new_cal.save()

        #the user probably wants to have a look at it. for now redirect to the admin-page
        return HttpResponseRedirect('../calibration/%s' % new_cal.id)

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        #we can only base it on one measurement
        if len(queryset) == 1:
            s = queryset.get()
            #this variable will hold all the values and is the address to the new measurement form
            redirect_address = u'add/?'
            #we don't want these to be adopted
            forbidden_items = ['_state', 'time', 'datafile']
            #walk through all fields of the model
            for item in s.__dict__:
                if item not in forbidden_items:
                    if s.__dict__[item] is not None:
                        redirect_address += http.urlquote(item) + '=' + http.urlquote(s.__dict__[item]) + '&'

            #redirect to newly created address
            return HttpResponseRedirect(redirect_address)
        else:
            messages.error(request, 'You can only base a new measurement on ONE existing measurement, stupid.')

class CalibrationAdmin(admin.ModelAdmin):
    readonly_fields = ('time', 'cal_base_file_1', 'formula', 'logoutput', 'p0', 'calibration_plot')
    ordering = ('-time',)

admin.site.register(Operator)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Calibration, CalibrationAdmin)
admin.site.register(JournalEntry)
