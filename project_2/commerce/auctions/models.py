from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bids(models.Model):
    date = models.DateTimeField()
    amount = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pass

class Comments(models.Model):
    date = models.DateTimeField()
    comment = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pass

class Listings(models.Model):
    price = models.FloatField()
    bids = models.ForeignKey(Bids, on_delete=models.CASCADE)
    lister = models.ForeignKey(User, on_delete=models.CASCADE)
    pass