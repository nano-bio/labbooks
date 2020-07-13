from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from stm.models import Image


@receiver(post_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.preview_image.delete(False)
