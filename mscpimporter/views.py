from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ExperimentMeasurementSelectForm
from .importer import ROOT_URL, LabbookImporter
from .models import MscpToken


def start_import(request):
    message = None
    if request.method == 'POST':
        form = ExperimentMeasurementSelectForm(request.POST)
        if form.is_valid():
            try:
                li = LabbookImporter(
                    int(form.data['measurement_id']),
                    form.data['mscp_token'],
                    form.data['experiment'])
                mscp_data_set_id = li.create_data_set()

                try:
                    token_obj = MscpToken.objects.first()
                    token_obj.token = form.data['mscp_token']
                    token_obj.save()
                except (ObjectDoesNotExist, AttributeError):
                    MscpToken.objects.create(token=form.data['mscp_token'])

                return HttpResponseRedirect(
                    f"{ROOT_URL}admin/node/dataset/{mscp_data_set_id}/change/")
            except Exception as e:
                message = ("danger", f"Error: {str(e)}")
        else:
            message = ("danger", f"Form data not valid: {form.errors}")
    else:
        form = ExperimentMeasurementSelectForm(initial={'mscp_token': get_token()})

    return render(request, 'mscpimporter/start.html', {'form': form, 'message': message, 'root_url': ROOT_URL})


def get_token():
    token_obj = MscpToken.objects.first()
    if token_obj:
        return token_obj.token
    else:
        return ""
