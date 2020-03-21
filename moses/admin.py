from django.contrib import admin

from moses.models import Target, File, Measurement


class MeasurementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_description', 'get_target', 'step_size', 'get_image_files', 'get_eval_files')
    list_filter = ('target',)
    search_fields = ('comment', 'short_description', 'id', 'target')
    readonly_fields = ('id',)
    save_on_top = True


class TargetAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_files')
    readonly_fields = ('id',)
    save_on_top = True


admin.site.register(Target, TargetAdmin)
admin.site.register(File)
admin.site.register(Measurement, MeasurementsAdmin)
