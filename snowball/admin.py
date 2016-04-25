#created after SurfTof
from django.contrib import admin, messages
from snowball.models import Measurement, Operator, JournalEntry, Turbopump, TurbopumpStatus
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, Template
from django.utils import http

import datetime

class MeasurementAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        return obj.time.strftime('%d %m %Y, %H:%M')
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
            'fields': ('operator', 'datafile', 'starttime', 'endtime')
        }),
#        ('Measurement', {
#            'fields': ('time',)
#        })
    )

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
        return obj.short.time.strftime('%d %m %Y, %H:%M')
    propertime.short_description = 'Time and date'

    list_display = ('propertime', 'operator', 'attachment', 'written_notes',)
    list_filter = ('operator', 'time',)
    serach_fields = ('comment',)
    save_as = True
    save_on_top = True
    ordering = ('-time',)

admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Operator,)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(Turbopump)
admin.site.register(TurbopumpStatus)
             
