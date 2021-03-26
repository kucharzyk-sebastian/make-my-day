from django.contrib import admin

from .models import Schedule, ScheduleEntry


class ScheduleEntryInline(admin.TabularInline):
    model = ScheduleEntry


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    inlines = [ScheduleEntryInline]


class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'day', 'start_time', 'end_time')

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(ScheduleEntry, ScheduleEntryAdmin)
