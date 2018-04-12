# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from stm.models import Sample, Measurement, Image, Operator, StandardOperatingProcedure

class MeasurementAdmin(admin.ModelAdmin):
    actions = ['read_images']

    def read_images(self, request, queryset):
        measurement = queryset.get()
        image_count = measurement.read_images()
        self.message_user(request, '{} images added'.format(image_count))

# Register your models here.
admin.site.register(Sample)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Image)
admin.site.register(Operator)
admin.site.register(StandardOperatingProcedure)
