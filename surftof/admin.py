from django.contrib import admin, messages
from surftof.models import Measurement, Operator, JournalEntry, Turbopump, TurbopumpStatus, VacuumStatus
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.loader import get_template
from django.template import Context, Template
from django.utils import http

import datetime
import re

class MeasurementAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        return obj.time.strftime('%d %m %Y, %H:%M')
    propertime.short_description = 'Time and date'

    list_display = ('propertime', 'operator', 'polarity', 'surface_material', 'projectile', 'collision_energy', 'data_file', 'evaluated_by', 'eval_file')
    list_filter = ('operator', 'time', 'polarity', 'evaluated_by', 'projectile')
    search_fields = ('surface_material', 'projectile', 'id')
    save_as = True
    save_on_top = True
    ordering = ('-time',)

    actions = ['create_new_measurement_based_on_existing_one', 'export_measurement', 'show_surrounding_data']

    fieldsets = (
        ('General', {
            'fields': ('operator', 'data_filename', 'polarity', 'time', 'evaluated_by', 'evaluation_file')
        }),
        ('Pressures', {
            'fields': ('pressure_is', 'pressure_surface', 'pressure_cube', 'pressure_tof'),
            'classes': ('wide',)
        }),
        ('Measurement', {
            'fields': ('u_surf', 'u_is', 'surface_material', 'projectile', 'surface_current', 'surface_temperature', 'heating_current'),
            'classes': ('wide',)
        }),
        ('ToF Settings', {
            'fields': ('fil_cur', 'fil_vol', 'far_cup', 'pusher_is', 'ion_block', 'zb1r', 'zb1l', 'zb_2', 'zyl1r', 'zyl1l', 'zyl2', 'def_ou', 'def_r', 'def_l', 'is_plate', 'pusher_tof', 'zl_grid', 'acc_grid', 'def_r_tof', 'def_l_tof', 'drift', 'reflectron', 'post_acc', 'mcp'),
        }),
    )

    def show_surrounding_data(self, request, queryset):
        s = queryset.first()
        earlier = s.time - datetime.timedelta(days=7)
        later = s.time + datetime.timedelta(days=7)

        adminurl = './?time__gte='+earlier.date().isoformat()+'&time__lt='+later.date().isoformat()
        return HttpResponseRedirect(adminurl)

    show_surrounding_data.short_description = u'Show data +/- one week'

    def export_measurement(self, request, queryset):
        #this is basically just a redirect
        if len(queryset) == 1:
            s = queryset.get()
            exporturl = 'http://' + settings.SURFTOFIP + '/' + s.data_filename.replace('D:\\Data\\','')
            return HttpResponseRedirect(exporturl)
        else:
            messages.error(request, 'You can only export ONE existing measurement, stupid.')

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        #we can only base it on one measurement
        if len(queryset) == 1:
            s = queryset.get()
            #this variable will hold all the values and is the address to the new measurement form
            redirect_address = u'add/?'
            #we don't want these to be adopted
            forbidden_items = ['_state', 'time', 'data_filename', 'rating']
            #walk through all fields of the model
            for item in s.__dict__:
                if item not in forbidden_items:
                    if s.__dict__[item] is not None:
                        redirect_address += http.urlquote(item) + '=' + http.urlquote(s.__dict__[item]) + '&'

            #redirect to newly created address
            return HttpResponseRedirect(redirect_address)
        else:
            messages.error(request, 'You can only base a new measurement on ONE existing measurement, stupid.')

class JournalEntryAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        return obj.time.strftime('%d %m %Y, %H:%M')
    propertime.short_description = 'Time and date'

    list_display = ('propertime', 'operator', 'attachment', 'written_notes')
    list_filter = ('operator', 'time')
    search_fields = ('comment',)
    save_as = True
    save_on_top = True
    ordering = ('-time',)

admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Operator)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(Turbopump)
admin.site.register(TurbopumpStatus)
admin.site.register(VacuumStatus)
