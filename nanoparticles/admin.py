import threading
from threading import Thread

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
        # 'open folder of file path,'
    ]

    @staticmethod
    def preview_image(obj):
        try:
            relative_url = MeasurementData.objects. \
                values_list('forward_z_axis_image', flat='True'). \
                get(measurement_id=obj.id)
            if not relative_url:
                raise MeasurementData.DoesNotExist()
            url = settings.MEDIA_URL + relative_url
        except MeasurementData.DoesNotExist:

            is_already_running = False
            for thread in threading.enumerate():
                if thread.name == f'thread_image_{obj.id}':
                    is_already_running = True

            if not is_already_running:
                x = Thread(target=extract_data_from_nid_file, args=(obj.id,))
                x.name = f'thread_image_{obj.id}'
                x.start()
                print("Started Thread")

            url = static('img/worker.png')
        return mark_safe(
            f'<a href"#">'
            f'<img src="{url}" width="{settings.NANOPARTICLES_PREVIEW_SIZE}" '
            f'height="{settings.NANOPARTICLES_PREVIEW_SIZE}">'
            f'</a>')


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Substrate)
admin.site.register(Coating)
