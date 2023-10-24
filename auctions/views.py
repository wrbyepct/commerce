from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, AuctionListing, Bid
from .forms import CustomUserCreationForm, NewListingForm
from .utils import print_normal_message, print_error_message

def index(request):
    listings = AuctionListing.objects.all()
    
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
            
            user.birthday = None if birthday == "" else birthday
            user.save()
            
        except IntegrityError:
            form = CustomUserCreationForm(request.POST)
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "form": form
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
   
    else:
        register_form = CustomUserCreationForm()
        return render(request, "auctions/register.html", {"form": register_form })


@login_required
def create_listing(request):
    
    if request.method == 'POST':
        
        form = NewListingForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            # Create instance from form
            listing = form.save(commit=False)
            # Save user 
            listing.poster = request.user 
            listing.save()
            
            # Create bid 
            bid = Bid.objects.create(
                auction_listing=listing,
                bid=listing.current_bid,
                user=request.user
            )
            
            bid.save()
            messages.success(request=request, message="Form's correct")
            return redirect('index')
            
            
        else:
            # Handle form's invalid
             ## Access the error messages 
            error_messages = form.errors.as_text()
            messages.error(request, error_messages)
            
   
    form = NewListingForm()
    # return an empty form 
    
    return render(request, 'auctions/create_listing.html', {'form': form})