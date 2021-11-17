from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from nanoparticles.helper import extract_data_from_nid_file
from nanoparticles.models import Measurement, Substrate, Coating, MeasurementData


class MeasurementAdmin(admin.ModelAdmin):
    list_filter = [
        'device',
        'substrate',
        'coating',
        'thickness',
        'sputter_time',
        'sputter_method',
        'time',
        'image_size',
        'rating',
        'spectroscopy',
        'conductivity',
        'xps']
    search_fields = [
        'comment',
        'file_path',
        'time',
        'coating',
        'substrate']
    list_display = [
        'time',
        'substrate',
        'coating',
        'thickness',
        'sputter_time',
        'sputter_method',
        'image_size',
        'preview_image',
        #    'open folder of file path,'
    ]

    def preview_image(self, obj):
        # return "asdf"
        try:
            m = MeasurementData.objects.get(measurement=obj)
            url = m.forward_z_axis_image.url
        except MeasurementData.DoesNotExist:
            # start thread for creating images
            extract_data_from_nid_file(measurement_id=obj.id)
            url = static('img/worker.png')
        return mark_safe(f'<a href"#">'
                         f'<img src="{url}" width="{settings.NANOPARTICLES_PREVIEW_SIZE}" '
                         f'height="{settings.NANOPARTICLES_PREVIEW_SIZE}">'
                         f'</a>')


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Substrate)
admin.site.register(Coating)
