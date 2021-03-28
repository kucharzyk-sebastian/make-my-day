from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class ScheduleTests(TestCase):
    def setUp(self):
        self.user_1 = get_user_model().objects.create_user(
            username='user1',
            email='user1@test.com',
            password='user1_password')

    def test_create_displays_sign_up_page(self):
        path = reverse('user_create')

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)

    def test_redirects_authenticated_user_to_home(self):
        path = reverse('user_create')
        self.client.login(username='user1', password='user1_password')

        response = self.client.get(path)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_create_redirects_to_home_after_signing_up(self):
        path = reverse('user_create')
        self.client.login(username='user1', password='user1_password')

        response = self.client.post(path, {
            'username': 'username',
            'email': 'user@email.com',
            'password': 'Longenoughpassword1!'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
