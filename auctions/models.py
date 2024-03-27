from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.category_name
    
class Listing(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 300)
    title = models.CharField(max_length = 50)
    image = models.CharField(max_length=600)
    price = models.IntegerField(max_length=30)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "owner")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True, related_name = "category")
    isActive = models.BooleanField(default=True)

class Bid(models.Model):
    bid = models.IntegerField(default = 0)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, blank = True, null = True, related_name = "bids")
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "user_bid")


class Comment(models.Model):
    comment = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listingComment')

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
    
class Watchlist(models.Model):
    items = models.ManyToManyField(Listing, blank=True, related_name="users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True, related_name = "user")