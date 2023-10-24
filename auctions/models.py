from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
import decimal

class User(AbstractUser):
    """User model with additional birthday field."""
    birthday = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"User info: Username: {self.username}, email: {self.email}, birthday: {self.birthday}"
    

class AuctionListing(models.Model):
    """Model for auction listings."""
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    current_bid = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        validators=[MinValueValidator(decimal.Decimal('0.01'))]
    )
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Medta:
        unique_together = ('poster', 'title')
    
    def __str__(self):
        return f"User {self.poster.username} opened an auction on item: {self.title} at {self.created_at}"


class Bid(models.Model):
    """Model for bids on auction listings."""
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="all_bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_bids")
    
    bid = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(decimal.Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.user.username} placed a new bid ${self.bid} on item: {self.auction_listing.title} at \
{self.created_at}"
    
    
class Comment(models.Model):
    """Model for comments on auction listings."""
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s comment on item: {self.auction_listing.title}"
        
    