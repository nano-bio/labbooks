from ckeditor.fields import RichTextField
from django.db import models
from django.utils.timezone import now


class JournalEntry(models.Model):
    time = models.DateTimeField(
        default=now)
    short_description = models.CharField(
        max_length=500)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='journal/journalImage/')
    image2 = models.ImageField(
        blank=True,
        null=True,
        upload_to='journal/journalImage/')
    image3 = models.ImageField(
        blank=True,
        null=True,
        upload_to='journal/journalImage/')
    image4 = models.ImageField(
        blank=True,
        null=True,
        upload_to='journal/journalImage/')
    image5 = models.ImageField(
        blank=True,
        null=True,
        upload_to='journal/journalImage/')
    file = models.FileField(
        blank=True,
        null=True,
        upload_to='journal/journalFiles/',
        verbose_name='File which can be downloaded')
    comment = RichTextField(
        blank=True)

    def __str__(self):
        if len(self.short_description) > 50:
            return f"ID {self.id}, {self.time.strftime('%Y-%m-%d %H:%M')}: {self.short_description[:45]}..."
        else:
            return f"ID {self.id}, {self.time.strftime('%Y-%m-%d %H:%M')}: {self.short_description}"

    class Meta:
        abstract = True
