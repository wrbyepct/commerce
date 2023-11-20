from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Bid, AuctionListing

@receiver(post_delete, sender=Bid)
def update_listing_on_bid_delete(sender, instance, **kwargs):
    if instance.auction_listing.current_bid_id == instance.id:
        # Get the highest bid that's still there
        highest_bid = instance.auction_listing.bids.order_by('-price').first()
        # Update the current_bid of the auction listing
        instance.auction_listing.current_bid = highest_bid
        instance.auction_listing.save()
        instance.auction_listing.refresh_from_db()


@receiver(post_delete, sender=AuctionListing)
def auction_listing_post_delete(sender, instance, **kwargs):
    category = instance.category
    
    # make sure a category exists only if there is at least one listing associated
    if category and not category.listings.exists():
        category.delete()
