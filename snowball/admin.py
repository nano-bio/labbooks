
from django.contrib import admin, messages
from snowball.models import Measurement, Operator, JournalEntry, Turbopump, TurbopumpStatus
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, Template
from django.utils import http
from django.conf import settings
from django.core.files import File
from django.db.models.fields.files import FieldFile
from django.contrib.admin.sites import AdminSite
from numpy import *

import os
import sys
import re
import datetime

class MeasurementAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        return obj.starttime.strftime('%d %m %Y, %H:%M')
    propertime.short_desctiption = 'Time and date'

    list_display = ('propertime', 'operator', 'datafile')
    list_filter = ('operator',)
    serach_fields = ('id',)
    save_as = True
    save_on_top = True
    ordering = ('-starttime',)

    actions = ['create_new_measurement_based_on_existing_one', 'export_measurement',]

    fieldsets = (
        ('General', {
            'fields': ('operator', 'datafile','he_temp', 'he_pres', 'ee', 'ec', 'starttime', 'com')
        }),)

    def export_measurement(self, request, queryset):
        if len(queryset) == 1:
            s = queryset.get()
            exporturl = 'http://' + settings.SNOWBALLIP + '/' + s.data_filename.replace('D://Data//','')
            return HttpResponseRedirect(exporturl)
        else:
            massages.error(request, 'You can only export ONE existing measurement, stupid.')

    def create_new_measurement_based_on_existing_one(self, request, queryset):
        if len(queryset) == 1:
            s = queryset.get()
            redirect_address = u'add/?'
            forbitten_item = ['_state', 'starttime', 'datafile']
            for item in s.__dict__:
                if item not in forbitten_items:
                    if s.__dict__[item] is not None:
                        redirect_address += http.urlquote(item) + '=' + http.urlquote(s.__dict__[item]) + '&'

            return HttpResponseRedirect(redirect_address)
        else:
            messages.error(request, 'You con only base a new measurement on ONE existing measurement, stupit.')

class JournalEntryAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        return obj.time.strftime('%d %m %Y, %H:%M')
    propertime.short_description = 'Time and date'

    list_display = ('propertime', 'operator', 'attachment', 'written_notes',)
    list_filter = ('operator', )
    serach_fields = ('comment',)
    save_as = True
    save_on_top = True
    ordering = ('-time',)


class PlotAdmin(admin.ModelAdmin):
    def openfile(filename, rw = 'r'):
        #adjust file path in case of Windows
        filename = os.path.nimcase(filename)

        try:
            #relativ path
            f = open(filename, rw)
            return f

        except:
            #full path
            try:
                f = open(filename, rw)
                return f
            except:
                raise IOError('Could not read this shit')

    def readfile(filename):
        list = []
        num_tab_num = re.compile('([0-9]{0,5}\.[0-9]{6})')
        for line in f:

           if not line.startswith('#'):
               result=num_tab_num.match(line)
               if result:
                   list.append(line.strip('\r\n).split(#\t'))
        data = array(a,dtype = float)
        f.close()
        data=array(list, dtype=float)
        return data

    def writefile(array, filename):
        f = openfile(filename, 'w')
        for valuepair in array:
            f.write('%f\t%f\r\n' % (valuepair[0], valuepair[1]))
        f.close()


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Operator,)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(Turbopump)
admin.site.register(TurbopumpStatus)
