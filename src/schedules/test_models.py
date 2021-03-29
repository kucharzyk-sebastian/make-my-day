from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from schedules.models import Schedule, ScheduleEntry


class TestSchedule(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test_user@test.com',
            password='test_password'
        )

    def test_can_be_created_with_all_fields(self):
        schedule_name = 'test_schedule'

        schedule = Schedule(name=schedule_name, author=self.user)
        schedule.full_clean()
        schedule.save()

    def test_has_name_as_string_representation(self):
        schedule_name = 'test_schedule'

        schedule = Schedule.objects.create(name=schedule_name, author=self.user)

        self.assertEqual(str(schedule), schedule_name)

    def test_name_size_is_constrained(self):
        too_long_schedule_name = 'a' * 101

        schedule = Schedule(name=too_long_schedule_name, author=self.user)

        with self.assertRaises(ValidationError):
            schedule.full_clean()

    def test_is_deleted_when_author_is_deleted(self):
        schedule_name = 'test_schedule'
        Schedule.objects.create(name=schedule_name, author=self.user)

        self.user.delete()

        with self.assertRaises(Schedule.DoesNotExist):
            Schedule.objects.get(name=schedule_name)


class TestScheduleEntry(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test_user@test.com',
            password='test_password'
        )
        self.schedule = Schedule.objects.create(name='test_schedule', author=self.user)

        self.schedule_entry_data = {
            'title': 'test_title',
            'description': 'test_description',
            'day': ScheduleEntry.DayInWeek.MONDAY,
            'start_time': '10:00:00',
            'end_time': '20:00:00'
        }

    def test_can_be_created_with_all_fields(self):
        schedule_entry = ScheduleEntry(schedule=self.schedule, **self.schedule_entry_data)
        schedule_entry.full_clean()
        schedule_entry.save()

    def test_can_be_created_without_optional_fields(self):
        self.schedule_entry_data.pop('description')

        ScheduleEntry.objects.create(schedule=self.schedule, **self.schedule_entry_data)

    def test_has_title_as_string_representation(self):
        schedule_entry = ScheduleEntry.objects.create(schedule=self.schedule, **self.schedule_entry_data)

        self.assertEqual(str(schedule_entry), self.schedule_entry_data['title'])

    def test_is_deleted_when_schedule_is_deleted(self):
        ScheduleEntry.objects.create(schedule=self.schedule, **self.schedule_entry_data)
        self.schedule.delete()

        with self.assertRaises(ScheduleEntry.DoesNotExist):
            ScheduleEntry.objects.get(title=self.schedule_entry_data['title'])

    @parameterized.expand([
        ('title', 'a' * 51),
        ('description', 'a' * 101),
        ('day', 'wrong_day'),
        ('start_time', '25:00'),
        ('end_time', '25:00')
    ])
    def test_fields_need_to_have_correct_values(self, field_name, value):
        self.schedule_entry_data[field_name] = value

        schedule = ScheduleEntry(schedule=self.schedule, **self.schedule_entry_data)

        with self.assertRaises(ValidationError):
            schedule.full_clean()

    @parameterized.expand([
        ('8:00', '8:00'),
        ('8:01', '8:00'),
    ])
    def test_start_time_must_be_before_end_time(self, start_time, end_time):
        self.schedule_entry_data['start_time'] = start_time
        self.schedule_entry_data['end_time'] = end_time

        schedule = ScheduleEntry(**self.schedule_entry_data)

        with self.assertRaises(ValidationError):
            schedule.full_clean()

    @parameterized.expand([
        ('starts_when_the_other_starts', '10:00', '13:00'),
        ('starts_in_the_middle_of_the_other', '11:00', '13:00'),
        ('ends_in_the_middle_of_the_other', '9:00', '11:00'),
        ('ends_when_the_other_ends', '9:00', '12:00'),
    ])
    def test_entry_cannot_overlap_with_another(self, _, start_time, end_time):
        initial_entry_data = self.schedule_entry_data.copy()
        initial_entry_data['start_time'] = '10:00'
        initial_entry_data['end_time'] = '12:00'
        ScheduleEntry.objects.create(schedule=self.schedule, **initial_entry_data)

        overlapping_entry_data = self.schedule_entry_data.copy()
        overlapping_entry_data['start_time'] = start_time
        overlapping_entry_data['end_time'] = end_time

        schedule = ScheduleEntry(**overlapping_entry_data)
        with self.assertRaises(ValidationError):
            schedule.full_clean()

    @parameterized.expand([
        ('starts_when_the_other_ends', '12:00', '13:00'),
        ('ends_when_the_other_starts', '9:00', '10:00'),
    ])
    def test_entry_can_be_scheduled_immediately_after_another(self, _, start_time, end_time):
        initial_entry_data = self.schedule_entry_data.copy()
        initial_entry_data['start_time'] = '10:00'
        initial_entry_data['end_time'] = '12:00'
        ScheduleEntry.objects.create(schedule=self.schedule, **initial_entry_data)

        new_entry_data = self.schedule_entry_data.copy()
        new_entry_data['start_time'] = start_time
        new_entry_data['end_time'] = end_time

        schedule_entry = ScheduleEntry(schedule=self.schedule, **new_entry_data)
        schedule_entry.full_clean()


    def test_entry_can_be_updated_within_the_same_time(self):
        schedule_entry = ScheduleEntry.objects.create(schedule=self.schedule, **self.schedule_entry_data)
        schedule_entry.title = 'new_title'

        schedule_entry.full_clean()
        schedule_entry.save()
