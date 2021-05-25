from django import forms

from surftof.models import JournalEntry, Measurement


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = '__all__'


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = '__all__'
