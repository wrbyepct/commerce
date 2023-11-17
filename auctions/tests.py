
# Create your tests here.
from django.test import TestCase
from .models import AuctionListing, Bid, User, Category

class BidSignalTest(TestCase):
    # When testing, Django use test database which is not yur local database 
    def setUp(self):
        # Create a user
        self.user = User.objects.create(username='testuser', password='12345', email="test@gmail.com")
        self.user2 = User.objects.create(username='testuser2', password='12345', email="test2@gmail.com")

        # Create a category (or use the default one if it already exists)
        category, created = Category.objects.get_or_create(name='TestCategory')

        # Create an AuctionListing instance
        self.listing = AuctionListing.objects.create(
            poster=self.user,
            title='Test Listing',
            description='This is a test listing.',
            category=category,
            # other fields as needed...
        )

        # Create Bid instances
        self.bid1 = Bid.objects.create(auction_listing=self.listing, price=100, user=self.user)
        self.bid2 = Bid.objects.create(auction_listing=self.listing, price=150, user=self.user2)

        # Set the current highest bid
        self.listing.current_bid = self.bid2
        self.listing.save()

    def test_bid_delete_signal(self):
        # Delete the highest bid
        self.user2.delete()

        # Refresh the listing from the database
        self.listing.refresh_from_db()

        # Check if the current_bid is updated correctly
        self.assertEqual(self.listing.current_bid, self.bid1)

        # Additional assertions can be made to verify other aspects of the signal's effect
