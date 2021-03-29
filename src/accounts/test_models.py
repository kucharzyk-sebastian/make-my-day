from django.test import TestCase

from accounts.models import CustomUser


class TestCustomUser(TestCase):
    @staticmethod
    def test_can_be_created_with_all_fields():
        user = CustomUser(username='test_user', email='test@email.cm', password='test_password')

        user.full_clean()
        user.save()

    def test_has_name_as_string_representation(self):
        user_name = 'test_user'

        user = CustomUser(username=user_name, email='test@email.cm', password='test_password')

        self.assertEqual(str(user), user_name)
