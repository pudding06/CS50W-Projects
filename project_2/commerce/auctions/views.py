from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Category


def index(request):
    listings = Listings.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings
    })


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
    
def create_listings(request):
    if request.method == "GET":
        all_catergorys = Category.objects.all()
        return render(request, "auctions/create_listings.html",{
            "all_catergorys": all_catergorys
        })
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = request.POST["category"]
        print(f"title: {title}\ndesc: {description}\nprice: {price}")

        # Save listing to database
        Listings.objects.create(
            owner=request.user,
            title=title,
            description=description,
            image=image,
            price=float(price),
            category=Category.objects.get(category_name=category)
        )
        return render(request, "auctions/index.html",{
            "listings": Listings.objects.all()
        })

def listing(request, id):
            listing = Listings.objects.get(id=id)
            isListingInWatchlist = request.user in listing.watchlist.all()

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "watchlist": isListingInWatchlist
            })

def add(request, id):
    listing = Listings.objects.get(id=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def remove(request, id):
    listing = Listings.objects.get(id=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))