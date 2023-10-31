# For frontend message
from django.contrib import messages

# For authentication 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST

# For saving instance to model 
from django.db import IntegrityError

# For return response 
from django.http import  HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


from decimal import Decimal
from .models import User, AuctionListing, Bid, Category, Comment
from .forms import CustomUserCreationForm, NewListingForm, PlaceBidForm, CommentForm
from .utils import print_normal_message, print_error_message

from .constants import *

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
        """
        Conditions:
            Required:
                1. title(text, 255↓) => Handle 
                2. description(text)
                3. user(User instance)
                4. category(Category instance): existing one, 
                Optional:
                    1. image(nullable)
            Actions:
                1. Save new listing 
        """
        form = NewListingForm(request.POST, request.FILES)
        
        if form.is_valid():
            category = form.cleaned_data['category']
            
            listing = form.save(commit=False)
            
            listing.category = category
            
            user = request.user
            # Save posting user
            listing.poster = user
            # Save listing while checking for integrity error(title, poster, category has to be unique)
            res = listing.save(failed_message=LISTING_NOT_UNIQUE)
            
            if res['status'] == 'failed':
                messages.error(request, res['message'])  
            
            else:    
    
                # Create & save bid 
                bid = Bid.objects.create(
                    auction_listing=listing,
                    price=form.cleaned_data['starting_bid'],
                    user=request.user
                )
                listing.current_bid = bid

                
                listing.save()
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
    
    listings = AuctionListing.objects.filter(poster=user_id).order_by('-updated_at')
    return render(request, 'auctions/my_postings.html', {'listings': listings})
    

def listing_page(request, listing_id):
    """
    Actions:
        1. Save current page listing id where the user is currently at.
        2. Provide:
            1. Listing instance
            2. Minimal bid for frotend(min attr) & backend(cleaned data) check
            3. Comment empty form 
            4. All commnets of this listing.
    """
    # Save listing ID in user session for later use.(Comment, close, place bid etc.)
    if request.user.is_authenticated:
        request.session['current_page_listing'] = listing_id
        
    # Handle GET method
    listing = AuctionListing.objects.get(id=listing_id)
    
    # Provide minimal bid
    minimal_bid = listing.current_bid.price + Decimal('0.01')
    
    place_bid_form = PlaceBidForm(custom_min_value=minimal_bid)
    
    comment_form = CommentForm()
    comments = listing.comments.all()

    
    return render(
        request, 
        'auctions/listing.html', 
        {
            'listing': listing,
            'place_bid_form': place_bid_form,
            'comment_form': comment_form,
            'comments': comments
        })
    

@login_required
def place_bid(request):
    if request.method == 'POST':
        # Check lising id first
        
        listing_id = request.session.get('current_page_listing')
        
        if listing_id is None:
            return HttpResponseForbidden("listing ID has lost")
        
        listing = AuctionListing.objects.get(id=listing_id)
        
        minimal_bid = listing.current_bid.price + Decimal('0.01')
        form = PlaceBidForm(request.POST, custom_min_value=minimal_bid)
        
        if form.is_valid(): 
            
            bid = form.cleaned_data['price']
            
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
    """
    Required: 
        1. current listing 
        2. highest bid user 
    Action:
        1. Update listing winner 
        2. Update listing status
    """
    if request.method == 'POST':
        
        listing_id = request.session.get('current_page_listing')
        if listing_id is None:
            return HttpResponseForbidden('Listing ID is somehow None')
        
        listing = AuctionListing.objects.get(id=listing_id)
        
        highest_bid = Bid.objects.filter(auction_listing=listing_id).order_by('-price').first()
       
        winner = highest_bid.user
        
        listing.winner = winner 
        listing.status = 'closed'
        
        listing.save()
        
        return redirect(reverse('listing', args=[listing_id]))

@login_required
def cancel_auction(request):
    """
    Required:
        1. Current page lisitng 
    """
    listing_id = request.session.get('current_page_listing')
    if listing_id is None:
        return HttpResponseForbidden('Listing ID is somehow None')
    
    listing = AuctionListing.objects.get(id=listing_id)
    
    listing.status = 'cancelled'
    listing.save()
    
    return redirect(reverse('listing', args=[listing_id]))


@login_required
@require_POST
def post_comment(request):
    """
    Required:
        1. listing id 
        2. Posting user 
        3. Valid commnet text
        
    Actions:
        1. Save comment instance 
    """
    listing_id = request.session.get('current_page_listing')
    if listing_id is None:
        return HttpResponseForbidden("Current page lisiting ID has somehow lost")
    
    
    form = CommentForm(request.POST)
    
    if form.is_valid():
        
        content = form.cleaned_data['content']
        listing = AuctionListing.objects.get(id=listing_id)
        user = request.user
        
        # Save commnet instance 
        comment = Comment(
            auction_listing=listing,
            user=user,
            content=content
        )
        
        res = comment.save(failed_message=COMMENT_SAVE_ERROR)
        if res['status'] == 'failed':
            messages.error(request, res['failed_message'])
            
        else:
            messages.success(request, f"The comment form is correct! your comment: {content}")
        
    else:
        messages.error(request, form.errors.as_text())
        
    return redirect(reverse('listing', args=[listing_id]))


@login_required
@require_POST
def delete_comment(request, comment_id):
    """
    Required:
        1. Comment id 
        2. User 
        3. Listing id 

    """
    listing_id = request.session.get('current_page_listing')
    if listing_id is None:
        messages.error(request, "The lisitng ID has somehow lost.")
    
    else:
        
        comment = get_object_or_404(Comment, id=comment_id)
        
        if comment.user != request.user:
            messages.error(request, "You are not authorized to delete this comment.")
        
        else:
            messages.success(request, 'Successfully deleted your comment!')
            comment.delete()
    
    return redirect(reverse('listing', args=[listing_id]))


@login_required
@require_POST
def provide_comment_content(request, comment_id):
    
    comment = get_object_or_404(Comment, comment_id)
    if comment.user != request.user:
        res = {
            'status': 'failed',
            'message': 'You are not authorized to delete this comment.'
        }
        
    else:
        res = {
            'status': 'success',
            'content': comment.content
        }
    return JsonResponse(res)


# @login_required
# @require_POST
# def change_comment_content(request, comment_id):
    
    
#     comment = get_object_or_404(Comment, comment_id)
#     if comment.user != request.user:
#         res = {
#             'status': 'failed',
#             'message': 'You are not authorized to delete this comment.'
#         }
        
#     else:
#         res = {
#             'status': 'success',
#             'content': comment.content
#         }
#     return JsonResponse(res)