# For frontend message
from django.contrib import messages

# For authentication 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# For saving instance to model 
from django.db import IntegrityError

# For return response 
from django.http import  HttpResponseRedirect, JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from django.core.signing import Signer

from decimal import Decimal
from .models import User, AuctionListing, Bid, Category
from .forms import CustomUserCreationForm, NewListingForm, PlaceBidForm
from .utils import print_normal_message, print_error_message

def index(request):
    listings = AuctionListing.objects.filter(status='open').order_by('-updated_at')
       
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]

        # Ensure password matches confirmation
        password = request.POST["password1"]
        confirmation = request.POST["password2"]
        
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
            )
            
        except IntegrityError:
            form = CustomUserCreationForm(request.POST)
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "form": form
            })
            
        user.birthday = birthday # Is empty string if leave unfilled
        user.save()    
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
   
    else:
        register_form = CustomUserCreationForm()
        return render(request, "auctions/register.html", {"form": register_form })


@login_required
def create_listing(request):
    
    if request.method == 'POST':
        
        form = NewListingForm(request.POST, request.FILES)
        # *title *description *category *bid
        # optional: 
        if form.is_valid():
            
            # Create instance from form
            listing = form.save(commit=False)
            # Saving title, description, image
            
            # Check new category 
            new_cate =form.cleaned_data.get('new_category').lower()
            if new_cate != "" and new_cate is not None:
                category = Category.objects.create(name=new_cate)
            
            else: 
                category = form.cleaned_data.get('category')            
            
            # Save category
            listing.category = category
            
            # Save user 
            listing.poster = request.user 
            
            # Save listing while checking for integrity error
            res = listing.save(message="You have created the a listing with the same title and category. Please ensure they are unique")
            
            if res['status'] == 'failed':
                messages.error(request, res['message'])  
            
            else:    
               
                # Create bid 
                bid = Bid.objects.create(
                    auction_listing=listing,
                    price=form.cleaned_data.get('starting_bid'),
                    user=request.user
                )
                
                listing.current_bid = bid
                
                res = listing.save()
                messages.success(request=request, message="Listing posted successfully!")
                return redirect('index')
            
        else:
            # Handle form's invalid
             ## Access the error messages 
            error_messages = form.errors.as_text()
            messages.error(request, error_messages)
            
    else:
        # GET
        # ## return an empty form 
        form = NewListingForm()
    
    return render(request, 'auctions/create_listing.html', {'form': form})

def categories(request):
    query = request.GET.get('category')
    
    if query is None:
        categories = Category.objects.all()
        return render(request, 'auctions/categories.html', {'categories': categories})
    
    category = Category.objects.get(name=query)
    listings = AuctionListing.objects.filter(category=category, status='open')
    return render(request, 'auctions/index.html', {'listings': listings})
    

@login_required
def watchlist(request): 
    user = request.user
    return render(request, 'auctions/watchlist.html', {'watchlist': user.watchlist.all()}) 

@login_required
def my_postings(request):
    user_id = request.user.id
    
    listings = AuctionListing.objects.filter(poster=user_id)
    return render(request, 'auctions/my_postings.html', {'listings': listings})
    


def listing_page(request, listing_id):
    if request.user.is_authenticated:
        request.session['current_page_listing'] = listing_id
    # Handle GET method
    listing = AuctionListing.objects.get(id=listing_id)
    
    # Provide minimal bid
    minimal_bid = listing.current_bid.price + Decimal('0.01')
    

    return render(
        request, 
        'auctions/listing.html', 
        {
            'listing': listing,
            'minimal_bid': minimal_bid
        })
    

@login_required
def place_bid(request):
    if request.method == 'POST':
        # Check lising id first
        
        listing_id = request.session.get('current_page_listing')
        
        if listing_id is None:
            return HttpResponseForbidden("listing ID has lost")
        
        form = PlaceBidForm(request.POST)
        
        if form.is_valid(): 
            
            bid = form.cleaned_data['bid_input']
            listing = AuctionListing.objects.get(id=listing_id)
            
            # Check submitted higher than currect bid
            if bid <= listing.current_bid.price:
                messages.error(request, "Invalid input. Your bid should be higher than current price")
                return redirect(reverse('listing', args=[listing_id]))
            
            # Save the new bid 
            new_bid = Bid.objects.create(
                auction_listing = listing,
                user = request.user,
                price = bid
            )
            new_bid.save()
            
            # update the listing current bid 
            listing.current_bid= new_bid
            listing.save()
            
            messages.success(request, f'Placed bid successfully! Your bid: {bid}')
            return redirect(reverse('listing', args=[listing_id]))
        else:
            messages.error(request, f"Not valid form: {form.errors.as_text()}")
            return redirect(reverse('listing', args=[listing_id]))


@login_required   
def toggle_watchlist(request):
    # Get listing id from user session
    listing_id = request.session.get('current_page_listing')
    if listing_id is None:
        return HttpResponseForbidden("listing ID has lost")
    
    if request.method == "POST":
        
        listing = AuctionListing.objects.get(id=listing_id)
        user = request.user
        
        # Add to watchlist
        if listing not in user.watchlist.all():
            user.watchlist.add(listing)
            res = {'status': 'added', 
                    'message': f"Added '{listing.title}' to watchlist"}
        else:
            # Remove from watchlists
            user.watchlist.remove(listing)
            res = {'status': 'removed', 
                    'message': f"Removed '{listing.title}' from watchlist"}
            
        return JsonResponse(res)

@login_required
def close_auction(request):
    if request.method == 'POST':
        
        listing_id = request.session.get('current_page_listing')
        if listing_id is None:
            return HttpResponseForbidden('Listing ID is somehow None')
        
        listing = AuctionListing.objects.get(id=listing_id)
        
        highest_bid = Bid.objects.filter(auction_listing=listing_id).order_by('-price').first()
        print(f"The highest bid of the listing: {listing.title}")
        print_normal_message(highest_bid)
        winner = highest_bid.user
        print(f"The winner of the bid: {winner}")
        
        listing.winner = winner 
        listing.status = 'closed'
        
        listing.save()
        
        return redirect(reverse('listing', args=[listing_id]))