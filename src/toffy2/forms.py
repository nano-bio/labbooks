from django import forms


class UpdateMeasurementRatingForm(forms.Form):
    id = forms.IntegerField()
    rating = forms.IntegerField()
