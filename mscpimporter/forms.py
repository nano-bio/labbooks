from django import forms

from mscpimporter.models import LABBOOK_EXPERIMENTS


class ExperimentMeasurementSelectForm(forms.Form):
    experiment = forms.ChoiceField(choices=LABBOOK_EXPERIMENTS)
    measurement_id = forms.IntegerField()
    mscp_token = forms.CharField(max_length=50)
