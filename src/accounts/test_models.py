from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import CustomUser


class TestCustomUser(TestCase):
    def test_can_be_created_with_all_fields(self):
        schedule = CustomUser(username='test_user', email='test@email.cm', password='test_password')

        schedule.full_clean()
        schedule.save()

    def test_has_name_as_string_representation(self):
        user_name = 'test_user'

        schedule = CustomUser(username=user_name, email='test@email.cm', password='test_password')

        self.assertEqual(str(schedule), user_name)
