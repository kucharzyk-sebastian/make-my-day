from django.urls import path

from .views import ScheduleCreateView, ScheduleDeleteView, ScheduleDetailView, ScheduleEntryCreate, ScheduleListView, ScheduleUpdateView

app_name = 'schedules'
urlpatterns = [
    path('', ScheduleListView.as_view(), name='schedule_list'),
    path('<int:pk>/delete', ScheduleDeleteView.as_view(), name='schedule_delete'),
    path('<int:pk>/edit', ScheduleUpdateView.as_view(), name='schedule_update'),
    path('<int:pk>/', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('create/', ScheduleCreateView.as_view(), name='schedule_create'),
    path('<int:schedule_id>/entries/create', ScheduleEntryCreate.as_view(), name='scheduleentry_create'),
]
