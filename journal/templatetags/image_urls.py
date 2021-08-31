from django import template

register = template.Library()


@register.simple_tag
def get_image_urls(journal_entry):
    image_urls = []
    for image in [
        journal_entry.image,
        journal_entry.image2,
        journal_entry.image3,
        journal_entry.image4,
        journal_entry.image5
    ]:
        if image:
            image_urls.append(image.url)
    return image_urls
