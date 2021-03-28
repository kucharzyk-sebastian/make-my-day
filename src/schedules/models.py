from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Schedule(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class ScheduleEntry(models.Model):
    class Meta:
        verbose_name_plural = "Schedule entries"
        ordering = ["day", "start_time"]

    class DayInWeek(models.TextChoices):
        MONDAY = 0, _('Monday')
        TUESDAY = 1, _('Tuesday')
        WEDNESDAY = 2, _('Wednesday')
        THURSDAY = 3, _('Thursday')
        FRIDAY = 4, _('Friday')
        SATURDAY = 5, _('Saturday')
        SUNDAY = 6, _('Sunday')

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    day = models.CharField(max_length=3, choices=DayInWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.title

    def clean(self):
        colliding = ScheduleEntry.objects.filter(
            day__exact=self.day,
            start_time__gte=self.start_time,
            start_time__lt=self.end_time
        )
        self._check_colliding(colliding)

        colliding = ScheduleEntry.objects.filter(
            day__exact=self.day,
            end_time__gt=self.start_time,
            end_time__lte=self.end_time
        )
        self._check_colliding(colliding)

        if self.start_time > self.end_time:
            raise ValidationError({'end_time': _('End time cannot be before start time.')})

    def _check_colliding(self, scheduled_entries):
        any_other_entry = not all([entry.pk == self.pk for entry in scheduled_entries])
        if any_other_entry:
            raise ValidationError({'start_time': _('You already have an entry in this time frame!!')})

