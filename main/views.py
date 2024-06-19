from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ServiceRequestForm, SearchForServicesOrCompany, BusinessProfileForm, ReviewForm
from .models import ServiceRequest, BusinessProfile, User, Review
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            login(request, user)
            return redirect('/home')  # Replace 'home' with your home view name
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')  # Replace 'home' with your home view name
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect("/login")

@login_required
def home(request):
    
    service_postings = ServiceRequest.objects.all()
    business_postings = BusinessProfile.objects.all()
    form = SearchForServicesOrCompany()  # Instantiate the search form

    if request.method == "POST":
        form = SearchForServicesOrCompany(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            if search_query:
                # Perform filtering based on search query
                service_postings = ServiceRequest.objects.filter(title__icontains=search_query)
                business_postings = BusinessProfile.objects.filter(industry__icontains=search_query)

            else:
                service_postings = ServiceRequest.objects.all()
                business_postings = BusinessProfile.objects.all()
            
            # Redirect or render after processing POST request
            return render(request, "main/dashboard.html", {'service_postings': service_postings, 'form': form, 'business_postings': business_postings})
    
    # Render the initial page with the form and listings
    return render(request, "main/dashboard.html", {'service_postings': service_postings, 'form': form, 'business_postings': business_postings})

@login_required
def delete(request):
    request.user.delete()

    logout(request)

    return redirect('/signup')  # Replace 'home' with your home view name

@login_required
def ServiceRequestPage(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            
            service_request = form.save(commit=False)
            service_request.user = request.user  # Set the user
            service_request.related_model = request.user  # Set the related_model
            service_request.save()

            
            return redirect('/success')
    else:
        form = ServiceRequestForm()
        
    return render(request, 'main/posting.html', {'form': form})
    
@login_required
def businessProfile(request):
    
    if request.user.profile.account_type == "business":
        # Check if the user already has a BusinessProfile
        try:
            business_profile = request.user.business_profile
        except BusinessProfile.DoesNotExist:
            business_profile = None

        if request.method == 'POST':
            form = BusinessProfileForm(request.POST, instance=business_profile)
            if form.is_valid():
                business_profile = form.save(commit=False)
                business_profile.user = request.user  # Associate with the current user
                business_profile.save()
                return redirect('/home')  # Redirect to a success page after saving
        else:
            form = BusinessProfileForm(instance=business_profile)

        return render(request, 'main/companyForm.html', {'form': form})

    return HttpResponse("<h1>This is only allowed for business owners</h1>")
   
def viewProfile(request, username):
    
    
    try:
        profile = User.objects.get(username=username)
        profile_type = 'user'
    except User.DoesNotExist:
        try:
            profile = BusinessProfile.objects.get(name=username)
            profile_type = 'business'
        except BusinessProfile.DoesNotExist:
            profile = None
            profile_type = None

    reviews = None
    if profile:
        if profile_type == 'user':
            reviews = Review.objects.filter(user=profile)
        elif profile_type == 'business':
            reviews = Review.objects.filter(BusinessProfile=profile)


    context = {
        'profile_type': profile_type,
        'profile': profile,
        'reviews': reviews,
    }
    
    return render(request, 'main/viewProfile.html', context)

def Profile(request):
    return render(request, 'main/posting.html')

#also do the same for posts
def success(request):
    return render(request, 'main/success.html')

@login_required
def review(request):
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            
            review = form.save(commit=False)
            review.user = request.user
            review.BusinessProfile = form.cleaned_data['business_profile']
            #print("Review data:", review.user, review.business_profile, review.rating, review.comment)
            review.save()
            
    else:
        form = ReviewForm()

    
    return render(request, "main/review.html", {"form":form})

