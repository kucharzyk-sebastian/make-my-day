from django.urls import path

from .views import ScheduleListView

app_name = 'schedules'
urlpatterns = [
    path('', ScheduleListView.as_view(), name='schedule_list')
]
