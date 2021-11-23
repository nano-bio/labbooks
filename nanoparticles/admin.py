from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from labbooks.admin_common import create_new_entry_based_on_existing_one_url
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
        'create_new_measurement_based_on_existing_one_inline',
        'substrate',
        'coating',
        'thickness',
        'sputter_time',
        'sputter_method',
        'image_size',
        'preview_image',
    ]

    def preview_image(self, obj):
        image_type = 'forward_z_axis_image'
        m_data = MeasurementData.objects \
            .filter(measurement_id=obj.id) \
            .values(image_type)

        if len(m_data) != 1:
            url = static('img/worker.png')
        else:
            relative_url = m_data[0][image_type]
            if relative_url:
                url = settings.MEDIA_URL + relative_url
            else:
                url = static('img/worker.png')

        return_str = mark_safe(
            f'<a href"#">'
            f'<img src="{url}" width="{settings.NANOPARTICLES_PREVIEW_SIZE}" '
            f'height="{settings.NANOPARTICLES_PREVIEW_SIZE}">'
            f'</a>')
        return return_str

    def create_new_measurement_based_on_existing_one_inline(self, s):
        forbidden_items = ['time', '_state']
        url = create_new_entry_based_on_existing_one_url(s, forbidden_items)
        return mark_safe(
            f"<a href='{url}' title='Duplicate this measurement'>"
            f"<img src='{static('images/clipboard-plus.svg')}'>"
            f"</a>")

    create_new_measurement_based_on_existing_one_inline.short_description = ""


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Substrate)
admin.site.register(Coating)
