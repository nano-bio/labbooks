from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from labbooks.admin_common import create_new_entry_based_on_existing_one_url
from nanoparticles.models import Measurement, Substrate, Coating, SputterMethod


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
        if obj.nid_file:
            url = settings.MEDIA_URL + f'nanoparticles/{obj.id}-Forward-Z-Axis.png"'

            return mark_safe(
                f'<a href"#">'
                f'<img src="{url}" width="{settings.NANOPARTICLES_PREVIEW_SIZE}" '
                f'height="{settings.NANOPARTICLES_PREVIEW_SIZE}">'
                f'</a>')
        else:
            return "No file uploaded."

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
admin.site.register(SputterMethod)
