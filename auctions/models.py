import decimal
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator

from .utils import integrity_check

class User(AbstractUser):
    """User model with additional birthday field."""
    birthday = models.DateField(null=True, blank=True)
    watchlist = models.ManyToManyField('AuctionListing', blank=True, related_name='watchers')
    
    def __str__(self):
        return f"User info: Username: {self.username}, email: {self.email}"
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True) # Ensure name of the instance is unique
    img_url = models.URLField(blank=True, null=True, default=None)
    
    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    class Meta:
        unique_together = ('poster', 'title', 'category')
        
    """Model for auction listings."""
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    
    winner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name="listings", on_delete=models.SET_DEFAULT, default=1) # default is 'other' category

    current_bid = models.ForeignKey('Bid', null=True, blank=True, on_delete=models.SET_NULL)
   
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"""User {self.poster.username} opened an auction on item: {self.title} at {self.created_at}
Cateogry: {self.category.name}   

"""
    
    @integrity_check
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
    
   

class Bid(models.Model):
    """Model for bids on auction listings."""
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(decimal.Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.user.username} placed a new bid ${self.price} on item: {self.auction_listing.title} at \
{self.created_at}"
    
    
class Comment(models.Model):
    """Model for comments on auction listings."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1024, validators=[MinLengthValidator(1)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    edited = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s comment on item: {self.auction_listing.title}"
    
    @integrity_check
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
        
    