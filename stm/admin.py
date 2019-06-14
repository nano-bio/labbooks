# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from stm.models import Sample, Measurement, Image, Operator, StandardOperatingProcedure
from stm.tasks import read_images_async


class ImageAdmin(admin.ModelAdmin):
    def stars(self, obj):
        if obj.image_rating:
            # UTF8 to the rescue!
            return '<span>{}{}</span>'.format(obj.image_rating * '★', (5 - obj.image_rating) * '☆')
        else:
            return ''

    stars.allow_tags = True

    def image_display(self, obj):
        try:
            return '<img src=\'{}\' style="max-height: 60px" />'.format(obj.preview_image.url)
        except ValueError:
            return ''

    image_display.allow_tags = True

    list_display = ('name', 'type', 'measurement', 'image_display', 'stars')
    list_filter = ('type', 'image_rating',)
    search_fields = ('measurement__name', 'measurement__sample__material', 'name')
    list_display_links = ('name', 'image_display')
    save_on_top = True


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'sample', 'name', 'operator', 'time', 'tip_type')
    list_filter = ('operator', 'time', 'tip_type')
    search_fields = ('sample', 'time', 'name')

    actions = ['read_images']

    def read_images(self, request, queryset):
        measurement = queryset.get()
        image_count, time_elapsed = read_images_async(measurement.id)
        self.message_user(request,
                          '{} images loading scheduled! Sceduling took {} seconds.'.format(image_count, time_elapsed))


# Register your models here.
admin.site.register(Sample)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Operator)
admin.site.register(StandardOperatingProcedure)
