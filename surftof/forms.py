from django import forms


class CreateCsvFileForm(forms.Form):
    id_list = forms.CharField(max_length=500, help_text="Use numbers, separated by comma only - (i.e. 9-11,13)")
    mass_list = forms.CharField(max_length=500, help_text="Use numbers, separated by comma only")
