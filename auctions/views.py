from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Category, Watchlist, Bid


def index(request):
    listings = Listing.objects.filter(isActive = True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def add_bid(request, id):
    listing = Listing.objects.get(pk=id)
    current_highest_bid = Bid.objects.filter(listing=listing).order_by('-bid').first()
    owner = listing.owner
    comments = Comment.objects.filter(listing = listing)
    watchlist = Watchlist.objects.get(user=request.user)
    listings_in_watchlist = watchlist.items.all()
    
    if request.method=='POST':
        user = request.user
        listing = Listing.objects.get(pk=id)
        user_bid = request.POST['user_bid']
        if current_highest_bid is None or int(user_bid) > (current_highest_bid.bid):
            new_bid = Bid(bid=int(user_bid), user=user, listing = listing)
            new_bid.save()
            current_highest_bid = new_bid
            return  render(request, "auctions/listing.html", {
                "listing": listing,
                "owner": owner,
                "comments": comments,
                "listings_in_watchlist": listings_in_watchlist,
                "user": user,
                "current_highest_bid": current_highest_bid,
                "message": "Bid was updated successfully!",
            })
        else:
            return  render(request, "auctions/listing.html", {
                "listing": listing,
                "owner": owner,
                "comments": comments,
                "listings_in_watchlist": listings_in_watchlist,
                "user": user,
                "current_highest_bid": current_highest_bid,
                "fail_message": "Bid failed to update. Bid is supposed to be higher than original price.",
            })
            
def close_auction(request, id):
    listing = Listing.objects.get(pk=id)
    current_highest_bid = Bid.objects.filter(listing=listing).order_by('-bid').first()
    owner = listing.owner
    comments = Comment.objects.filter(listing = listing)
    watchlist = Watchlist.objects.get(user=request.user)
    listings_in_watchlist = watchlist.items.all()
    user = request.user
    listing.isActive = False
    listing.save()
    if request.method=='POST':
        return  render(request, "auctions/listing.html", {
            "listing": listing,
            "owner": owner,
            "comments": comments,
            "listings_in_watchlist": listings_in_watchlist,
            "user": user,
            "current_highest_bid": current_highest_bid,
            "close_message": "Auction is closed!",

            })

def add_watchlist(request, id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=id)
        user = request.user
        watchlist, created = Watchlist.objects.get_or_create(user=user)
        watchlist.items.add(listing)
        return HttpResponseRedirect(reverse("watchlist"))
    
def delete_watchlist(request, id):
    if request.method == 'POST':
        user = request.user
        watchlist = Watchlist.objects.get(user = user)
        listing = Listing.objects.get(pk=id)
        watchlist.items.remove(listing)
        
        return HttpResponseRedirect(reverse("watchlist"))
    
def watchlist(request):
    user = request.user
    watchlist, created = Watchlist.objects.get_or_create(user=user)
    listings_in_watchlist = watchlist.items.all()
    return render(request, "auctions/watchlist.html", { 
        "watchlist": watchlist,
        "listings": listings_in_watchlist,
    })

def listing(request, id): 
    if request.method == 'GET':
        listing_info = Listing.objects.get(pk=id)
        owner = listing_info.owner
        comments = Comment.objects.filter(listing = listing_info)
        user = request.user
        current_highest_bid = Bid.objects.filter(listing=listing_info).order_by('-bid').first()
        return  render(request, "auctions/listing.html", {
                "listing": listing_info,
                "owner": owner,
                "comments": comments,
                "user": user,
                "current_highest_bid": current_highest_bid
            })
    else:
        listing_info = Listing.objects.get(pk=id)
        owner = listing_info.owner
        comments = Comment.objects.filter(listing = listing_info)
        user = request.user
        watchlist, created = Watchlist.objects.get_or_create(user=user)
        listings_in_watchlist = watchlist.items.all()
        current_highest_bid = Bid.objects.filter(listing=listing_info).order_by('-bid').first()
        return  render(request, "auctions/listing.html", {
                "listing": listing_info,
                "owner": owner,
                "comments": comments,
                "listings_in_watchlist": listings_in_watchlist,
                "user": user,
                "current_highest_bid": current_highest_bid
            })


def add_comment(request, id):
    if request.method =='GET':
        listing = Listing.objects.get(pk=id)
        return HttpResponseRedirect(reverse("listing", args=[id]))
    if request.method == 'POST':
        author = request.user
        listing = Listing.objects.get(pk=id)
        comment = request.POST['comment']
        new_comment = Comment(
            author = author,
            listing = listing,
            comment = comment
        )
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=[id]))

def category(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "auctions/category.html", {
            "categories": categories
        })
    if request.method == 'POST':
        cat = request.POST['category']
        category = Category.objects.get(category_name = cat)
        listings = Listing.objects.filter(isActive = True, category = category)
        categories = Category.objects.all()
        return render(request, "auctions/category.html", {
            "listings": listings,
            "categories": categories
        })
     
def create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            'categories': categories
        })
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        image = request.POST['image']
        category = request.POST['category']
        user = request.user
        category_data = Category.objects.get(category_name = category)
        bid = Bid(bid = int(price), user=user)
        bid.save()
        new_listing = Listing(
            title = title,
            description = description,
            price = price,
            category = category_data,
            owner = user,
            image = image
        )
        new_listing.save()

        return HttpResponseRedirect(reverse(index))
    
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
