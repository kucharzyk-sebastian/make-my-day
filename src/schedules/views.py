from django.views.generic import ListView

from .models import Schedule


class ScheduleListView(ListView):
    model = Schedule

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
