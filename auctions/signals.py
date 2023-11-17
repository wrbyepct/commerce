from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Bid

@receiver(post_delete, sender=Bid)
def update_listing_on_bid_delete(sender, instance, **kwargs):
    if instance.auction_listing.current_bid_id == instance.id:
        # Get the highest bid that's still there
        highest_bid = instance.auction_listing.bids.order_by('-price').first()
        # Update the current_bid of the auction listing
        instance.auction_listing.current_bid = highest_bid
        instance.auction_listing.save()
        instance.auction_listing.refresh_from_db()
