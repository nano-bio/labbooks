from wippi.models import *
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files import File
from django.db.models.fields.files import FieldFile

from django.contrib.admin.sites import AdminSite

import sys
sys.path.append('/var/opt/')

import fitlib

class MeasurementAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        return obj.time.strftime('%d %m %Y, %H:%M')
    propertime.short_description = 'Time and date'

    list_display = ('propertime', 'substance', 'description', 'scantype', 'datafile')
    list_filter = ('operator', 'time', 'scantype')
    search_fields = ('substance', 'description')
    save_as = True
    save_on_top = True
    ordering = ('-time',)

    actions = ['create_new_quadratic_calibration', 'create_new_linear_calibration', 'create_new_measurement_based_on_existing_one']

    fieldsets = (
        ('General', {
            'fields': ('operator', 'datafile', 'scantype', 'polarity', 'substance', 'description', 'time')
        }),
        ('Pressures', {
            'fields': ('pressure_monochromator', 'pressure_pickup', 'pressure_cs', 'background_pressure'),
            'classes': ('wide',)
        }),
        ('Quadrupole Lenses', {
            'fields': ('ion_energy', 'optics_inside', 'optics_outside', 'def_a', 'def_i', 'field_axis'),
            'classes': ('wide',)
        }),
        ('WIPPI settings', {
            'fields': ('channeltron_1', 'channeltron_2', 'oven_temperature', 'chamber_temperature', 'faraday_current', 'filament_current', 'electron_energy', 'emission', 'energy_resolution', 'mass_resolution'),
            'classes': ('wide',)
        }),
        ('Lenses', {
            'fields': ('anode', 'coil_voltage_xy', 'coil_voltage_xz', 'coil_voltage_yz', 'coil_current_xy', 'coil_current_xz', 'coil_current_yz', 'lens_1a', 'lens_1b', 'lens_1c', 'lens_A1', 'lens_L2', 'lens_L3', 'lens_2a', 'lens_2b', 'lens_2c', 'lens_L4', 'lens_L5', 'lens_D1', 'lens_D2', 'lens_Ua', 'lens_Ui', 'uhk_mitte', 'lens_3a', 'lens_3b', 'lens_3c', 'lens_A2', 'lens_L6', 'lens_L7', 'lens_4a', 'lens_4b', 'lens_4c', 'lens_L8', 'uex_mitte', 'lens_A3', 'lens_L10', 'lens_SK1', 'lens_SK2'),
            'classes': ('wide',)
        }),
        ('Comments', {
            'fields': ('comments',),
            'classes': ('wide',)
        })
    )

    def create_new_calibration(self, request, queryset, quadratic):

        if len(queryset) < 3:
            messages.error(request, 'Choose at least 3 Measurements to create a new calibration')
        else:
            #let's set up an empty calibration right away and save it, so we can get the id. we need that to save the file
            new_cal = Calibration(p0 = 0, p1 = 0, p2 = 0)
            new_cal.save()

            #first we get all the corresponding filenames and measurement_IDs to the measurements selected
            filelist = []
            id_list = []

            for cal_measurement in queryset.all():
                filelist.append(settings.MEDIA_ROOT + cal_measurement.datafile.name)
                #separate list because fitlib only wants a list with filenames
                id_list.append(cal_measurement.id)

            #create a unique filename
            filename = settings.MEDIA_ROOT + 'wippi/calibrations/' + str(new_cal.id) + '.pdf'

            #actually try some fitting
            parameters, log = fitlib.SF6_calibration.do_SF6_calibration(filelist, showplots = False, quadratic = quadratic, outputfile = filename)

            #create a FieldFile object
            f = open(filename)
            new_cal.calibration_plot.save(filename, File(f))

            #create an easily copy-pastable formula
            if quadratic is True:
                formula = 'y = %s + %s*x + %s*x^2' % (parameters[0], parameters[1], parameters[2])
            else:
                formula = 'y = %s + %s*x' % (parameters[0], parameters[1])

            #fill our new calibration with the values retrieved from fitlib
            new_cal.logoutput = log
            new_cal.p0 = parameters[0]
            new_cal.p1 = parameters[1]
            if quadratic is True:
                new_cal.p2 = parameters[2]
            else:
                new_cal.p2 = 0
            new_cal.formula = formula
            new_cal.cal_base_file_1 = Measurement.objects.get(id = id_list[0])
            new_cal.cal_base_file_2 = Measurement.objects.get(id = id_list[1])
            new_cal.cal_base_file_3 = Measurement.objects.get(id = id_list[2])
            #only if we actually had 4 files
            if len(id_list) == 4:
                new_cal.cal_base_file_4 = Measurement.objects.get(id = id_list[3])

            #last but not least: save it
            new_cal.save()

        #the user probably wants to have a look at it. for now redirect to the admin-page
        return HttpResponseRedirect('../calibration/%s' % new_cal.id)

    #the next two functions are merely wrappers for create_new_calibration()
    #because action-functions cannot have any other arguments than self, request, queryset

    def create_new_linear_calibration(self, request, queryset):
        return self.create_new_calibration(request, queryset, False)

    def create_new_quadratic_calibration(self, request, queryset):
        return self.create_new_calibration(request, queryset, True)

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        #we can only base it on one measurement
        if len(queryset) == 1:
            s = queryset.get()
            #this variable will hold all the values and is the address to the new measurement form
            redirect_address = 'add/?'
            #we don't want these to be adopted
            forbidden_items = ['_state', 'time', 'datafile']
            #walk through all fields of the model
            for item in s.__dict__:
                if item not in forbidden_items:
                    if s.__dict__[item] is not None:
                        redirect_address += item + '=' + str(s.__dict__[item]) + '&'

            #redirect to newly created address
            return HttpResponseRedirect(redirect_address)
        else:
            messages.error(request, 'You can only base a new measurement on ONE existing measurement, stupid.')

class CalibrationAdmin(admin.ModelAdmin):
    readonly_fields = ('time', 'cal_base_file_1', 'cal_base_file_2', 'cal_base_file_3', 'cal_base_file_4', 'formula', 'logoutput', 'p0', 'p1', 'p2', 'calibration_plot')
    ordering = ('-time',)

admin.site.register(Operator)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Calibration, CalibrationAdmin)
admin.site.register(JournalEntry)
