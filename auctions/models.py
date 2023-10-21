from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True)



class AuctionListings(models.Model):
    pass 



class Bids(models.Model):
    pass
    
    
class Comment(models.Model):
    pass