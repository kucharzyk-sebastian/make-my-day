from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.urls import reverse

from .models import Schedule


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
