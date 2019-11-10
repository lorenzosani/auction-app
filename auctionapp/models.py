from django.contrib.auth.models import User
from django.db import models

# Extend User class to inherit useful fields.
# Namely username, password and email
class Member(User):
    date_of_birth = models.DateField()
    def __str__(self):
        return "Username: {}".format(self.username)