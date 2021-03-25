from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ Easily extensible custom user model """

    def __str__(self):
        return str(self.username)
