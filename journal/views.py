from datetime import timedelta

from django.db.models import Model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from surftof.models import JournalEntry as JournalEntrySurftof
from toffy.models import JournalEntry as JournalEntryToffy
from toffy2.models import JournalEntry as JournalEntryToffy2


def homepage(request):
    journal_models = [
        JournalEntrySurftof,
        JournalEntryToffy,
        JournalEntryToffy2
    ]
    experiments = [
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


class JournalEntryUpdate(UpdateView):
    fields = '__all__'
    model: Model = None  # define the Journal Model from an experiment
    template_name = 'journal/journal_entry_form.html'

    def get_success_url(self):
        return reverse_lazy(f'{self.model._meta.app_label}-journal')


class JournalEntryDelete(DeleteView):
    model: Model = None  # define the Journal Model from an experiment
    template_name = 'journal/journal_confirm_delete.html'
    experiment: str = None  # set the verbose experiment name, which will be shown on the page

    def get_success_url(self):
        return reverse_lazy(f'{self.model._meta.app_label}-journal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment'] = self.experiment
        return context


class JournalEntryCreate(CreateView):
    model: Model = None  # define the Journal Model from an experiment
    template_name = 'journal/journal_entry_form.html'
    experiment: str = None  # set the verbose experiment name, which will be shown on the page
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy(f'{self.model._meta.app_label}-journal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiment'] = self.experiment
        return context
