from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def get_image_urls(journal_entry):
    image_urls = []
    for image in [
        journal_entry.image1,
        journal_entry.image2,
        journal_entry.image3,
        journal_entry.image4,
        journal_entry.image5
    ]:
        if image:
            image_urls.append(image.url)
    if journal_entry.measurement:
        try:
            image_urls.append(
                reverse(
                    "journal-mass-spec-preview-image",
                    args=(journal_entry._meta.app_label, journal_entry.measurement.id)
                ))
        except:
            print('no working mass spec preview url found')
    return image_urls
