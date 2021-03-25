from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.urls import reverse

from .models import Schedule, ScheduleEntry


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    fields = ('name', )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('schedules:schedule_detail', args=[self.object.pk])


class ScheduleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Schedule

    def test_func(self):
        return self.get_object().author == self.request.user


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    fields = ('name', )

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('schedules:schedule_detail', args=[self.object.pk])


class ScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Schedule
    success_url = '/'

    def test_func(self):
        return self.get_object().author == self.request.user


class ScheduleEntryCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ScheduleEntry
    fields = ('title', 'description', 'day', 'start_time', 'end_time')

    def test_func(self):
        self.schedule = get_object_or_404(Schedule, pk=self.kwargs['schedule_id'])
        return self.schedule.author == self.request.user

    def form_valid(self, form):
        form.instance.schedule = self.schedule
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('schedules:schedule_detail', args=[self.object.schedule.pk])


class ScheduleEntryDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ScheduleEntry

    def test_func(self):
        schedule = get_object_or_404(Schedule, pk=self.kwargs['schedule_id'])
        return schedule.author == self.request.user

    def get_success_url(self):
        return reverse('schedules:schedule_detail', args=[self.object.schedule.pk])
