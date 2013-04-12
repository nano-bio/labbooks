from vg.models import *
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.conf import settings

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
    ordering = ('-time',)

    actions = ['create_new_calibration']

    fieldsets = (
        ('General', {
            'fields': ('operator', 'datafile', 'scantype', 'substance', 'description', 'time')
        }),
        ('Pressures', {
            'fields': ('pressure_ionblock', 'pressure_analyzer'),
            'classes': ('wide',)
        }),
        ('VG settings', {
            'fields': ('channeltron', 'ionblock_temperature', 'trap_current', 'filament_current'),
            'classes': ('wide',)
        }),
        ('Voltages Ionsource', {
            'fields': ('ion_repeller', 'focus_coarse_1', 'focus_coarse_2', 'focus_fine_1', 'focus_fine_2', 'deflector_1', 'deflector_2'),
            'classes': ('wide',)
        }),
        ('Voltages Analyer', {
            'fields': ('ion_energy', 'y_focus', 'x_deflect', 'z_deflect', 'curve_1', 'rotate_1', 'z_deflect_1', 'z_focus_1', 'curve_2', 'rotate_2', 'z_deflect_2', 'z_focus_2'),
            'classes': ('wide',)
        }),
        ('Comments', {
            'fields': ('comments',),
            'classes': ('wide',)
        })
    )

    def create_new_calibration(self, request, queryset):

        if len(queryset) <= 2:
            messages.error(request, 'Choose at least 2 Measurements to create a new calibration')
        else:
            #let's set up an empty calibration right away and save it, so we can get the id. we need that to save the file
            new_cal = Calibration(cal_base_file_1_id = 1, cal_base_file_2_id = 1, cal_base_file_3_id = 1, cal_base_file_4_id = 1, p0 = 0, p1 = 0, p2 = 0)
            new_cal.save()

            #first we get all the corresponding filenames and measurement_IDs to the measurements selected
            filelist = []
            id_list = []

            for cal_measurement in queryset.all():
                filelist.append(settings.MEDIA_ROOT + cal_measurement.datafile.name)
                #separate list because fitlib only wants a list with filenames
                id_list.append(cal_measurement.id)

            #create a unique filename
            new_cal.calibration_plot.name = settings.MEDIA_ROOT + 'vg/calibrations/' + str(new_cal.id) + '.pdf'

            #actually try some fitting
            parameters, log = fitlib.SF6_calibration.do_SF6_calibration(filelist, showplots = False, quadratic = True, outputfile = new_cal.calibration_plot.name)

            #create an easily copy-pastable formula
            formula = 'y = %s + %s*x + %s*x^2' % (parameters[0], parameters[1], parameters[2])

            #fill our new calibration with the values retrieved from fitlib
            new_cal.logoutput = log
            new_cal.p0 = parameters[0]
            new_cal.p1 = parameters[1]
            new_cal.p2 = parameters[2]
            new_cal.formula = formula
            new_cal.cal_base_file_1 = Measurement.objects.get(id = id_list[0])
            new_cal.cal_base_file_2 = Measurement.objects.get(id = id_list[1])
            new_cal.cal_base_file_3 = Measurement.objects.get(id = id_list[2])
            new_cal.cal_base_file_4 = Measurement.objects.get(id = id_list[3])

            #last but not least: save it
            new_cal.save()

        #the user probably wants to have a look at it. for now redirect to the admin-page
        return HttpResponseRedirect('../calibration/%s' % new_cal.id)

class CalibrationAdmin(admin.ModelAdmin):
        readonly_fields = ('time', 'cal_base_file_1', 'cal_base_file_2', 'cal_base_file_3', 'cal_base_file_4', 'formula', 'logoutput', 'p0', 'p1', 'p2', 'calibration_plot')

admin.site.register(Operator)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Calibration, CalibrationAdmin)
