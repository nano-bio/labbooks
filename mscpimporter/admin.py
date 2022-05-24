from django.contrib import admin

from mscpimporter.models import MscpToken, Experiment

admin.site.register(MscpToken)
admin.site.register(Experiment)
