from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .forms import ContactForm, SignupForm
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect("djangoapp:thanks")

    form = ContactForm()
    return render(request, 'djangoapp/contact.html', {'form': form})

def thanks(request):
    return render(request, 'djangoapp/thanks.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
        else:
            # If not, return to login page again
            messages.error(request, "Unable to authenticate user")
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user_exists = False
            username = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            try:
            # Check if user already exists
                User.objects.get(username=username)
                user_exists = True
            except:
                logger.debug("{} is new user".format(username))
            # If it is a new user
            if not user_exists:
                # Create user in auth_user table
                user = User.objects.create_user(
                    username=username, 
                    first_name=first_name, 
                    last_name=last_name,
                    password=password, 
                    email=email
                )
                return redirect("djangoapp:index") 
    
    form = SignupForm()
    return render(request, 'djangoapp/registration.html', {'form': form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://davismike37-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', {'dealer_names': dealer_names})


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://davismike37-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealer = get_dealer_by_id_from_cf(url, id=dealer_id)
        context["dealer"] = dealer
    
        review_url = "https://davismike37-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(review_url, dealerId=dealer_id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, id):
    if request.user.is_authenticated:
        context = {}
        dealer_url = "https://davismike37-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealer = get_dealer_by_id_from_cf(dealer_url, id)
        context["dealer"] = dealer
        if request.method == "GET":
            cars = CarModel.objects.all()
            context["cars"] = cars
            print(context)
            return render(request, 'djangoapp/add_review.html', context)
        
        if request.method == "POST":
            review = {}
            review["name"] = request.user.first_name + " " + request.user.last_name
            form = request.POST
            review["dealership"] = id
            review["review"] = form["content"]
            if(form.get("purchasecheck") == "on"):
                review["purchase"] = True
            else:
                review["purchase"] = False
            if(review["purchase"]):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year
            post_url = "https://davismike37-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            json_payload = { "review": review }
            post_request(post_url, json_payload, id=id)
            return redirect("djangoapp:dealer_details", id=id)
    else:
        me
        return redirect('djangoapp:index')

def get_user_profile(request):
    return render(request, 'djangoapp/index.html')