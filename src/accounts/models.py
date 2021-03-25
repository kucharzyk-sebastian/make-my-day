from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ Easily extensible custom user model """
