from django.contrib import admin, messages
from clustof.models import Comment, Measurement, Operator, CurrentSetting, JournalEntry, Turbopump, TurbopumpStatus, VacuumStatus
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.loader import get_template
from django.template import Context, Template
from django.utils import http

import datetime
import re
import pytz
from operator import attrgetter

class CommentInline(admin.TabularInline):
    model = Comment

class MeasurementAdmin(admin.ModelAdmin):
    def propertime(self, obj):
        mtime = obj.time.astimezone(pytz.timezone('Europe/Vienna'))
        return mtime.strftime('%d %m %Y, %H:%M')
    propertime.short_description = 'Time and date'

    def has_comment(self, obj):
        comments = Comment.objects.filter(measurement = obj).all()
        if len(comments) >= 1:
            return True
        else:
            return False

    has_comment.boolean = True
    has_comment.short_description = 'Com.'

    def eval_by(self, obj):
        return obj.evaluated_by

    def EE(self, obj):
        return obj.elec_energy()

    list_display = ('propertime', 'id', 'marked', 'operator', 'scantype', 'chems', 'substance', 'polarity', 'EE', 'temperature_he', 'data_file', 'has_comment', 'eval_by', 'eval_file')
    list_filter = ('operator', 'time', 'scantype', 'polarity', 'evaluated_by', 'marked')
    search_fields = ('substance', 'data_filename', 'tof_settings_file', 'id', 'chem_pu1_oven__name', 'chem_pu1_oven__chemical_formula', 'chem_pu2_oven__name', 'chem_pu2_oven__chemical_formula', 'chem_pu1_gas__name', 'chem_pu1_gas__chemical_formula', 'chem_pu2_gas__name', 'chem_pu2_gas__chemical_formula', 'is_inlet_gas__name', 'is_inlet_gas__chemical_formula')
    readonly_fields = ('id',)
    save_as = True
    save_on_top = True
    ordering = ('-time',)

    inlines = [CommentInline]

    actions = ['create_new_measurement_based_on_existing_one', 'export_measurement', 'show_surrounding_data', 'scan_properties', 'export_frequencies']

    fieldsets = (
        ('General', {
            'fields': ('id', ('operator', 'operator2', 'operator3'), 'data_filename', 'tof_settings_file', 'scantype', 'time', ('evaluated_by', 'evaluation_file'), ('flagged', 'marked'), 'rating')
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
            'fields': ('electron_energy_set', 'real_electron_energy', 'ion_block', 'pusher', 'wehnelt', ('extraction_1', 'extraction_1_left', 'extraction_1_right'), 'extraction_2', 'deflector_1', 'deflector_2', 'filament_current', 'trap_current', 'housing_current', 'faraday_cup', 'polarity'),
            'classes': ('wide',)
        }),
        ('Pickup', {
            'fields': (('oven_1_temperature', 'oven_1_power'), ('oven_2_temperature', 'oven_2_power'), ('chem_pu1_oven', 'chem_pu1_gas'), ('chem_pu2_oven', 'chem_pu2_gas'), 'is_inlet_gas', 'substance'),
            'classes': ('wide',)
        }),
    )

    def chems(self, obj):
        chems = [obj.chem_pu1_oven, obj.chem_pu1_gas, obj.chem_pu2_oven, obj.chem_pu2_gas, obj.is_inlet_gas]
        chems_used = filter(None, chems)
        chem_string = u' '.join(map(attrgetter('chemical_formula'), chems_used))
        return chem_string

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
            exporturl = 'http://' + settings.CLUSTOFIP + '/' + s.data_filename.replace('D:\\Data\\','')
            return HttpResponseRedirect(exporturl)
        else:
            messages.error(request, 'You can only export ONE existing measurement, stupid.')

    def export_frequencies(self, request, queryset):
        datasets = queryset.all()
        values = []
        regex = '([0-9]{3},[0-9]{2,6}[ ]?)(n|N)(m|M)'
        prog = re.compile(regex)
        for dataset in datasets:
            fn = dataset.data_filename
            result = prog.search(dataset.substance)
            if result:
                frequency = result.group(1)
                filename = str(dataset.id) + ' ' + str(frequency).replace('nm', '') + ' ' + str(fn).replace('D:\\Data\\','') + '\n'
                values.append(filename.replace('  ', ' '))

        return HttpResponse(values)


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

    def scan_properties(self, request, queryset):
        measurements = queryset.all().order_by('id')
        t = get_template('clustof/scan_properties.html')
        c = Context({'measurements': measurements})

        html = t.render(c)

        return HttpResponse(html)

    scan_properties.short_description = u'Export measurement properties'

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

class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('measurement',)

admin.site.register(Comment, CommentAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Operator)
admin.site.register(CurrentSetting)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(Turbopump)
admin.site.register(TurbopumpStatus)
admin.site.register(VacuumStatus)
