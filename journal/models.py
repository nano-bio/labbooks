from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse_lazy
from django.utils.timezone import now


class BasicJournalEntry(models.Model):
    time = models.DateTimeField(
        default=now)
    title = models.CharField(
        max_length=500)
    operator = models.ForeignKey(
        'Operator',
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    image1 = models.ImageField(
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
    measurement = models.ForeignKey(
        'Measurement',
        blank=True,
        null=True,
        on_delete=models.PROTECT)
    comment = RichTextField(
        blank=True)

    def __str__(self):
        if len(self.title) > 50:
            return f"ID {self.id}, {self.time.strftime('%Y-%m-%d %H:%M')}: {self.title[:45]}..."
        else:
            return f"ID {self.id}, {self.time.strftime('%Y-%m-%d %H:%M')}: {self.title}"

    def url_form_update(self):

        return reverse_lazy(f'{self._meta.app_label}-journal-update', args=(self.pk,))

    def url_form_add(self):
        return reverse_lazy(f'{self._meta.app_label}-journal-add')

    def url_form_delete(self):
        return reverse_lazy(f'{self._meta.app_label}-journal-delete', args=(self.pk,))

    def url_measurement_admin_change(self):
        if self.measurement:
            return reverse_lazy(f'admin:{self._meta.app_label}_measurement_change', args=(self.pk,))

    def url_mass_spec(self):
        if self.measurement:
            return reverse_lazy(f'{self._meta.app_label}-mass-spectra') + f'?id={self.measurement.id}'

    class Meta:
        abstract = True
