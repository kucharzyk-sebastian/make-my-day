from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from schedules.models import Schedule, ScheduleEntry


class ScheduleTests(TestCase):

    def setUp(self):
        self.user_1 = get_user_model().objects.create_user(
            username='user1',
            email='user1@test.com',
            password='user1_password')
        self.schedule_1 = Schedule.objects.create(
            name="user1_schedule",
            author=self.user_1
        )


        self.user_2 = get_user_model().objects.create_user(
            username='user2',
            email='user2@test.com',
            password='user2_password')
        self.schedule_2 = Schedule.objects.create(
            name="user2_schedule",
            author=self.user_2
        )

    def test_list_redirects_unauthenticated_users_to_login(self):
        path = '/'
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('login')}?next={path}")

    def test_list_returns_list_of_user_schedules(self):
        path = '/'
        self.client.login(username='user1', password='user1_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1_schedule')
        self.assertNotContains(response, 'user2_schedule')

    def test_create_redirects_unauthenticated_users_to_login(self):
        path = reverse('schedules:schedule_create')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('login')}?next={path}")

    def test_create_lets_in_authenticated_user(self):
        path = reverse('schedules:schedule_create')
        self.client.login(username='user1', password='user1_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)

    def test_create_redirects_to_detail_view(self):
        path = reverse('schedules:schedule_create')
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path, {'name': 'new_schedule_name'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('schedules:schedule_detail', args=[3]))

    def test_detail_redirects_unauthenticated_users_to_login(self):
        path = reverse('schedules:schedule_detail', args=['1'])
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('login')}?next={path}")

    def test_detail_displays_schedule_for_the_owner(self):
        path = reverse('schedules:schedule_detail', args=['1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1_schedule')

    def test_detail_does_not_allow_to_see_other_users_schedule(self):
        path = reverse('schedules:schedule_detail', args=['1'])
        self.client.login(username='user2', password='user2_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 403)

    def test_update_redirects_unauthenticated_users_to_login(self):
        path = reverse('schedules:schedule_update', args=['1'])
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('login')}?next={path}")

    def test_update_lets_in_authenticated_owner(self):
        path = reverse('schedules:schedule_update', args=['1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1_schedule')

    def test_update_does_not_allow_to_update_other_users_schedule(self):
        path = reverse('schedules:schedule_update', args=['1'])
        self.client.login(username='user2', password='user2_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 403)

    def test_update_redirects_to_detail_view(self):
        path = reverse('schedules:schedule_update', args=['1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path, {'name': 'new_schedule_name'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('schedules:schedule_detail', args=[1]))

    def test_update_fails_on_not_existing_schedule(self):
        path = reverse('schedules:schedule_update', args=['123'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path, {'name': 'new_schedule_name'})

        self.assertEqual(response.status_code, 404)

    def test_delete_redirects_unauthenticated_users_to_login(self):
        path = reverse('schedules:schedule_delete', args=['1'])
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('login')}?next={path}")

    def test_delete_lets_in_authenticated_owner(self):
        path = reverse('schedules:schedule_delete', args=['1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1_schedule')

    def test_delete_does_not_allow_to_delete_other_users_schedule(self):
        path = reverse('schedules:schedule_delete', args=['1'])
        self.client.login(username='user2', password='user2_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 403)

    def test_delete_redirects_to_list_view(self):
        path = reverse('schedules:schedule_delete', args=['1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('schedules:schedule_list'))

    def test_delete_fails_on_not_existing_schedule(self):
        path = reverse('schedules:schedule_delete', args=['123'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path)

        self.assertEqual(response.status_code, 404)


class ScheduleEntryTests(TestCase):

    def setUp(self):
        self.user_1 = get_user_model().objects.create_user(
            username='user1',
            email='user1@test.com',
            password='user1_password')
        self.schedule_1 = Schedule.objects.create(
            name="user1_schedule",
            author=self.user_1
        )
        self.schedule_1_entry = ScheduleEntry.objects.create(
            schedule = self.schedule_1,
            title = 'entry_1_title',
            day = ScheduleEntry.DayInWeek.TUESDAY,
            start_time = '10:00',
            end_time = '12:00'
        )

        self.user_2 = get_user_model().objects.create_user(
            username='user2',
            email='user2@test.com',
            password='user2_password')
        self.schedule_2 = Schedule.objects.create(
            name="user2_schedule",
            author=self.user_2
        )

    def test_create_redirects_unauthenticated_users_to_login(self):
        path = reverse('schedules:scheduleentry_create', args=['1'])
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('login')}?next={path}")

    def test_create_lets_in_authenticated_owner(self):
        path = reverse('schedules:scheduleentry_create', args=['1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)

    def test_create_does_not_allow_to_update_other_users_schedule_entry(self):
        path = reverse('schedules:scheduleentry_create', args=['1'])
        self.client.login(username='user2', password='user2_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 403)

    def test_create_redirects_to_detail_view(self):
        path = reverse('schedules:scheduleentry_create', args=['1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path, {
            'schedule': self.schedule_1,
            'title': 'new_title',
            'day': ScheduleEntry.DayInWeek.TUESDAY,
            'start_time': '16:00',
            'end_time': '19:00'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('schedules:schedule_detail', args=[1]))

    def test_create_detects_missing_parent_schedule(self):
        path = reverse('schedules:scheduleentry_create', args=['123'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path, {
            'schedule': self.schedule_1,
            'title': 'new_title',
            'day': ScheduleEntry.DayInWeek.TUESDAY,
            'start_time': '16:00',
            'end_time': '19:00'})

        self.assertEqual(response.status_code, 404)

    def test_delete_redirects_unauthenticated_users_to_login(self):
        path = reverse('schedules:scheduleentry_delete', args=['1', '1'])
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('login')}?next={path}")

    def test_delete_lets_in_authenticated_owner(self):
        path = reverse('schedules:scheduleentry_delete', args=['1', '1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'entry_1_title')

    def test_delete_does_not_allow_to_delete_other_users_schedule(self):
        path = reverse('schedules:scheduleentry_delete', args=['1', '1'])
        self.client.login(username='user2', password='user2_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 403)

    def test_delete_redirects_to_schedule_view(self):
        path = reverse('schedules:scheduleentry_delete', args=['1', '1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('schedules:schedule_detail', args=['1']))

    def test_delete_detects_missing_parent_schedule(self):
        path = reverse('schedules:scheduleentry_delete', args=['123', '1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path)

        self.assertEqual(response.status_code, 404)

    def test_delete_fails_on_missing_schedule_entry(self):
        path = reverse('schedules:scheduleentry_delete', args=['1', '123'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path)

        self.assertEqual(response.status_code, 404)

    def test_update_redirects_unauthenticated_users_to_login(self):
        path = reverse('schedules:scheduleentry_update', args=['1', '1'])
        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('login')}?next={path}")

    def test_update_lets_in_authenticated_owner(self):
        path = reverse('schedules:scheduleentry_update', args=['1', '1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)

    def test_update_does_not_allow_to_update_other_users_schedule_entry(self):
        path = reverse('schedules:scheduleentry_update', args=['1', '1'])
        self.client.login(username='user2', password='user2_password')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 403)

    def test_update_redirects_to_detail_view(self):
        path = reverse('schedules:scheduleentry_update', args=['1', '1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path, {
            'schedule': self.schedule_1,
            'title': 'new_title',
            'day': ScheduleEntry.DayInWeek.TUESDAY,
            'start_time': '16:00',
            'end_time': '19:00'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('schedules:schedule_detail', args=[1]))

    def test_update_detects_missing_parent_schedule(self):
        path = reverse('schedules:scheduleentry_update', args=['123', '1'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path, {
            'schedule': self.schedule_1,
            'title': 'new_title',
            'day': ScheduleEntry.DayInWeek.TUESDAY,
            'start_time': '16:00',
            'end_time': '19:00'})

        self.assertEqual(response.status_code, 404)

    def test_update_detects_missing_schedule_entry(self):
        path = reverse('schedules:scheduleentry_update', args=['1', '123'])
        self.client.login(username='user1', password='user1_password')
        response = self.client.post(path, {
            'schedule': self.schedule_1,
            'title': 'new_title',
            'day': ScheduleEntry.DayInWeek.TUESDAY,
            'start_time': '16:00',
            'end_time': '19:00'})

        self.assertEqual(response.status_code, 404)
