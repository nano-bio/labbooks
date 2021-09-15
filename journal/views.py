import traceback
from datetime import timedelta
from io import BytesIO

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from clustof.models import JournalEntry as JournalEntryClustof
from clustof.views import get_mass_spectrum as get_mass_spectrum_clustof
from massspectra.views import get_mass_spectrum_from_csv
from surftof.helper import get_mass_spectrum as get_mass_spectrum_surftof
from surftof.models import JournalEntry as JournalEntrySurftof
from toffy.models import JournalEntry as JournalEntryToffy, Measurement as MeasurementToffy
from toffy2.models import JournalEntry as JournalEntryToffy2, Measurement as MeasurementToffy2


def homepage(request):
    journal_models = [
        JournalEntryClustof,
        JournalEntrySurftof,
        JournalEntryToffy,
        JournalEntryToffy2
    ]
    experiments = [
        'ClusTof',
        'SurfTof',
        'Toffy',
        'Toffy 2'
    ]

    all_journal_entries = []
    for journal_entry_model in journal_models:
        all_journal_entries += journal_entry_model.objects.filter(time__gte=now() - timedelta(days=30))

    all_journal_entries.sort(key=lambda x: x.time, reverse=False)
    for i in all_journal_entries:
        i.experiment = str(i._meta).split('.')[0].capitalize()

    return render(
        request,
        template_name='journal/homepage.html',
        context={
            'journal_entries': all_journal_entries,
            'experiments': ', '.join(experiments),
        }
    )


class JournalListView(ListView):
    template_name = 'journal/journal_experiment.html'
    paginate_by = 20
    model: Model = None  # define the Journal Model from an experiment
    experiment: str = None  # set the verbose experiment name, which will be shown on the page
    ordering = '-id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment'] = self.experiment
        context['add_url'] = reverse_lazy(f'{self.model._meta.app_label}-journal-add')
        return context


class JournalEntryUpdate(PermissionRequiredMixin, UpdateView):
    fields = '__all__'
    model: Model = None  # define the Journal Model from an experiment
    template_name = 'journal/journal_entry_form.html'

    def get_success_url(self):
        return reverse_lazy(f'{self.model._meta.app_label}-journal')

    def get_permission_required(self, **kwargs):
        return f'{self.model._meta.app_label}.change_journalentry',


class JournalEntryDelete(PermissionRequiredMixin, DeleteView):
    model: Model = None  # define the Journal Model from an experiment
    template_name = 'journal/journal_confirm_delete.html'
    experiment: str = None  # set the verbose experiment name, which will be shown on the page

    def get_success_url(self):
        return reverse_lazy(f'{self.model._meta.app_label}-journal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment'] = self.experiment
        return context

    def get_permission_required(self, **kwargs):
        return f'{self.model._meta.app_label}.delete_journalentry',


class JournalEntryCreate(PermissionRequiredMixin, CreateView):
    model: Model = None  # define the Journal Model from an experiment
    template_name = 'journal/journal_entry_form.html'
    experiment: str = None  # set the verbose experiment name, which will be shown on the page
    fields = '__all__'

    def get_permission_required(self, **kwargs):
        return f'{self.model._meta.app_label}.add_journalentry',

    def get_success_url(self):
        return reverse_lazy(f'{self.model._meta.app_label}-journal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment'] = self.experiment
        return context


def mass_spec_preview_image(request, experiment, measurement_id):
    try:
        mass_max = float(request.COOKIES['previewMassMax'])
    except (KeyError, ValueError):  # use defaults
        mass_max = 200
    try:
        use_log = request.COOKIES['previewShowLog'].lower() in ['true', '1', 't']
    except (KeyError, ValueError):  # use defaults
        use_log = False
    try:
        pixel_width = int(request.COOKIES['previewWidth'])
    except (KeyError, ValueError):  # use defaults
        pixel_width = 550
    try:
        pixel_height = int(request.COOKIES['previewHeight'])
    except (KeyError, ValueError):  # use defaults
        pixel_height = 250
    try:
        show_x_axis = request.COOKIES['previewShowMassAxis'].lower() in ['true', '1', 't']
    except (KeyError, ValueError):  # use defaults
        show_x_axis = True

    try:
        content = get_mass_spectrum_preview_image(
            experiment,
            measurement_id,
            mass_max,
            use_log,
            pixel_height,
            pixel_width,
            show_x_axis)

        html = HttpResponse(content, content_type="image/png")

    except:
        traceback.print_exc()
        html = HttpResponse(status=404, content="could not create image preview")

    html.set_cookie('previewMassMax', f'{mass_max}', max_age=None)
    html.set_cookie('previewShowLog', f"{use_log}", max_age=None)
    html.set_cookie('previewWidth', f"{pixel_width}", max_age=None)
    html.set_cookie('previewHeight', f"{pixel_height}", max_age=None)
    html.set_cookie('previewShowMassAxis', f"{show_x_axis}", max_age=None)
    return html


def get_mass_spectrum_preview_image(
        experiment,
        measurement_id,
        mass_max,
        use_log,
        pixel_height,
        pixel_width,
        show_x_axis):
    # get XY Data from mass spectra for the right experiment
    if experiment == 'surftof':
        xs, ys = get_mass_spectrum_surftof(
            measurement_id=measurement_id,
            mass_max=mass_max)
    elif experiment == 'toffy':
        file_1 = MeasurementToffy.objects.get(pk=measurement_id).data_file.path
        xs, ys = get_mass_spectrum_from_csv(file_1)
    elif experiment == 'toffy2':
        file_1 = MeasurementToffy2.objects.get(pk=measurement_id).data_file.path
        xs, ys = get_mass_spectrum_from_csv(file_1)
    elif experiment == 'clustof':
        xs, ys = get_mass_spectrum_clustof(
            measurement_id=measurement_id,
            mass_max=mass_max)
    else:
        raise Exception('No proper experiment name given')

    if len(xs) == len(ys) and len(xs) > 2:

        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from matplotlib.figure import Figure
        fig = Figure(figsize=(pixel_width / 100, pixel_height / 100))
        ax = fig.subplots()
        if use_log:
            ax.semilogy(xs, ys)
        else:
            ax.plot(xs, ys)

        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(show_x_axis)

        fig.subplots_adjust(left=0, right=1, bottom=int(show_x_axis) * 25 / pixel_height, top=1)

        with BytesIO() as pseudo_file:
            FigureCanvas(fig).print_png(pseudo_file)
            return pseudo_file.getvalue()
