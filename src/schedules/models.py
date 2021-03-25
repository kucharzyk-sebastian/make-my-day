from django.contrib.auth import get_user_model
from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
