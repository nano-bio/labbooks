from django.db import models
from django.utils.html import format_html


class File(models.Model):
    name = models.CharField(max_length=30)
    file = models.FileField(
        blank=True,
        upload_to="moses")

    def __str__(self):
        return self.name


class Target(models.Model):
    name = models.CharField(
        max_length=100)
    files = models.ManyToManyField(
        File,
        blank=True,
        related_name='target_image')
    comment = models.TextField(
        max_length=1000,
        blank=True)

    def __str__(self):
        return self.name

    def get_files(self):
        return return_file_links(self.files.all())

    get_files.short_description = "images"


class Measurement(models.Model):
    short_description = models.CharField(
        max_length=200)
    target = models.ForeignKey(
        Target,
        on_delete=models.PROTECT)
    image = models.ManyToManyField(
        File,
        verbose_name="Evaluated Image",
        related_name='image',
        blank=True)
    evaluation_file = models.ManyToManyField(
        File,
        help_text="Zip evaluation files",
        related_name='evaluation_file',
        blank=True)
    step_size = models.IntegerField(
        help_text="Unit: micro meter")

    def __str__(self):
        if len(self.short_description) > 15:
            return "ID {}, {}...".format(self.id, self.short_description[:10])
        else:
            return "ID {}, {}".format(self.id, self.short_description)

    def get_eval_files(self):
        return return_file_links(self.evaluation_file.all())

    def get_image_files(self):
        return return_file_links(self.image.all())

    def get_target(self):
        return format_html("<a href='/admin/moses/target/'>{}</a>".format(self.target.name))

    get_eval_files.short_description = "Eval. files"
    get_image_files.short_description = "Images"
    get_target.short_description = "Target"


def return_file_links(many_to_many_list):
    links = []
    for file in many_to_many_list:
        links.append("<a target='_blank' href='{}'>{}</a>".format(file.file.url, file.name))
    return format_html("<br>".join(links))
