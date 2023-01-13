import csv
import threading
from os import makedirs
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.db.models import ForeignKey
from django.forms.utils import pretty_name
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify

from clustof import models as clustof_models
from toffy import models as toffy_models
from toffy2 import models as toffy2_models


def create_new_entry_based_on_existing_one_url(s, forbidden_items):
    # this variable will hold all the values and is the address to the new setting form
    redirect_address = u'add/?'

    # walk through all fields of the model
    for item in s.__dict__:
        if item not in forbidden_items:  # we don't want these to be adopted
            if s.__dict__[item] is not None:
                # ForeignKey fields have to be named without "_id", so the last 3 chars are truncated
                if "id" in quote(item) and len(quote(item)) > 2:
                    redirect_address += quote(item)[:-3] + '=' + quote(str(s.__dict__[item])) + '&'
                else:
                    redirect_address += quote(item) + '=' + quote(str(s.__dict__[item])) + '&'
    return redirect_address


def create_new_entry_based_on_existing_one(request, queryset, forbidden_items):
    # we can only base it on one measurement
    if len(queryset) == 1:
        s = queryset.get()
        # redirect to newly created address
        return HttpResponseRedirect(create_new_entry_based_on_existing_one_url(s, forbidden_items))
    else:
        messages.error(request, 'You can only base a new entry on ONE existing setting, stupid.')


def export_tables_csv(experiment_media_root, model):
    def is_not_empty_foreignkey(obj, field):
        return obj.__getattribute__(field.name) and \
            isinstance(field, ForeignKey)

    def str_foreignkey_with_id(obj, field):
        return f"#{obj.__getattribute__(field.name).pk} {obj.__getattribute__(field.name).__str__()}"

    def get_field_value(obj, field):
        if is_not_empty_foreignkey(obj, field):
            return str_foreignkey_with_id(obj, field)
        else:
            return obj.__getattribute__(field.name)

    makedirs(experiment_media_root, exist_ok=True)
    csv_filename = experiment_media_root / f'export-{slugify(model._meta.verbose_name)}.csv'
    with open(csv_filename, 'w') as f:
        writer = csv.writer(f)
        field_names = [field.name for field in model._meta.fields]
        writer.writerow([pretty_name(field_name) for field_name in field_names])
        objs = model.objects.all()
        for row in objs:
            writer.writerow([get_field_value(row, field) for field in model._meta.fields])


def export_tables_csv_all():
    # CLUSTOF
    for model in [
        clustof_models.Measurement,
        clustof_models.Operator,
        clustof_models.JournalEntry,
    ]:
        export_tables_csv(settings.MEDIA_ROOT / 'clustof', model)

    # TOFFY
    for model in [
        toffy_models.Measurement,
        toffy_models.Operator,
        toffy_models.JournalEntry,
    ]:
        export_tables_csv(settings.MEDIA_ROOT / 'toffy', model)

    # TOFFY2
    for model in [
        toffy2_models.Measurement,
        toffy2_models.Operator,
        toffy2_models.JournalEntry,
    ]:
        export_tables_csv(settings.MEDIA_ROOT / 'toffy2', model)


def export_tables_csv_view(request):
    thread_name = "thread-export-csv"
    if request.method == 'POST':
        threading.Thread(
            target=export_tables_csv_all,
            daemon=True,
            name=thread_name
        ).start()
        running = True
    else:
        running = is_process_already_running(thread_name)
    return render(request, 'export_tables_csv.html', {'running': running})


def is_process_already_running(process_name: str) -> bool:
    for thread in threading.enumerate():
        if process_name in thread.name:
            return True
    return False
