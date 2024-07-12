from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.TextField()

    def __str__ (self):
        return f"{self.category_name}"

class Listings(models.Model):
    price = models.FloatField()
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", blank=True, null=True)
    image = models.URLField()
    title = models.CharField(max_length=40, default="New listing")
    isActive = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingwatchlist")

    def __str__ (self):
        return self.title