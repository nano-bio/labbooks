from django import forms

from toffy.models import JournalEntry


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = '__all__'
