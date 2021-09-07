import csv
import itertools

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from toffy.forms import JournalEntryForm
from toffy.models import Measurement, JournalEntry


# ------------
# Mass Spectra
# ------------
class MassSpectraListView(ListView):
    paginate_by = 15
    model = Measurement
    template_name = 'massspectra/mass_spectra_viewer.html'

    def get_context_data(self, **kwargs):
        context = super(MassSpectraListView, self).get_context_data(**kwargs)
        context['experiment'] = 'TOFFY'
        context['admin_measurement_url'] = reverse_lazy('admin:toffy_measurement_changelist')
        return context


def preview_data(request, pk):
    obj = get_object_or_404(Measurement, id=int(pk))
    reader = csv.reader(open(obj.data_file.path, 'r'), delimiter="\t")
    xy_data = []
    for line in reader:
        xy_data.append([
            float(line[0]),
            int(float(line[1]))])
    return JsonResponse({'data': xy_data, 'id': obj.id, 'datetime': obj.time.strftime('%d.%m.%Y %H:%M')}, safe=False)


def preview_file_list(request):
    # get all measurements from DB
    objects = Measurement.objects.order_by('-time')

    response = []
    for key, group in itertools.groupby(objects, key=lambda x: x.time.date()):

        tmp = {'date': key, 'times': []}
        for val in group:
            if val.data_file:
                tmp['times'].append({
                    'time': val.time.strftime('%H:%M'),
                    'id': val.id,
                    'downloadUrl': "{}".format(val.data_file.url)})
        response.append(tmp)
    return JsonResponse(response, safe=False)


def preview_measurement_info(request, measurement_id):
    obj = get_object_or_404(Measurement, pk=measurement_id)
    data = {
        'measurementId': obj.id,
        'fields': {
            "Short Description": obj.short_description,
            "Comment": obj.comment,
            "Evaporation gas pressure [mbar]": f"{obj.evaporation_pressure:.2e}",
        }
    }
    return JsonResponse(data, safe=False)


class JournalListView(ListView):
    paginate_by = 20
    model = JournalEntry

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment'] = "Toffy"
        context['add_url'] = reverse_lazy('toffy-journal-add')
        context['journal_change_url'] = reverse_lazy('toffy-journal-update', args=(1,))[:-2]
        context['admin_measurement_url'] = reverse_lazy('admin:toffy_measurement_change', args=(1,))[:-9]
        context['journal_delete_url'] = reverse_lazy('toffy-journal-delete', args=(1,))[:-9]
        return context


class JournalEntryUpdate(UpdateView):
    form_class = JournalEntryForm
    model = JournalEntry
    template_name = 'journal/journal_entry_form.html'
    success_url = reverse_lazy('toffy-journal')


class JournalEntryDelete(DeleteView):
    form_class = JournalEntryForm
    model = JournalEntry
    template_name = 'journal/journal_confirm_delete.html'
    success_url = reverse_lazy('toffy-journal')


class JournalEntryCreate(CreateView):
    form_class = JournalEntryForm
    template_name = 'journal/journal_entry_form.html'
    success_url = reverse_lazy('toffy-journal')
