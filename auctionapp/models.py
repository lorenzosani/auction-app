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
    start_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    end_time = models.DateTimeField()
    bids = models.ManyToManyField(Member, through='Bid')
    def __str__(self):
        return "Item: {}".format(self.title)


#A bid is a many-to-many relationship between Member and Item;
#The intermediate class Bid stores all extra info needed.
class Bid(models.Model):
    bidder = models.ForeignKey(Member, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_placed = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} -> {} (£{})".format(self.bidder.username, self.item.title, self.amount)
    class Meta:
        ordering = ['-amount']
        get_latest_by = "-time_placed"




    