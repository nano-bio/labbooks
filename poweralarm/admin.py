from django.contrib import admin
from poweralarm.models import Experiment

# Register your models here.
class ExperimentAdmin(admin.ModelAdmin):
    filter_horizontal = ['persons',]

admin.site.register(Experiment, ExperimentAdmin)
