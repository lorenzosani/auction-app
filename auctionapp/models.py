from django.contrib.auth.models import User
from django.db import models

# Extend User class to inherit useful fields.
# Namely username, password and email
class Member(User):
    date_of_birth = models.DateField()
    def __str__(self):
        return "Username: {}".format(self.username)


class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='item_images')
    end_time = models.DateTimeField()
    def __str__(self):
        return "Item: {}".format(self.title)
    