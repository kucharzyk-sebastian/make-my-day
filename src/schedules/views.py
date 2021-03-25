from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Schedule


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
