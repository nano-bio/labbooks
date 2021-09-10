from django import template

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
            image_urls.append(journal_entry.measurement.get_mass_spec_image_url())
        except:
            pass
    return image_urls
