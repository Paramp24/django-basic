
from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ServiceRequest, BusinessProfile, Profile, Review

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    account_type = forms.ChoiceField(choices=[('individual', 'Individual'), ('business', 'Business')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'account_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, account_type=self.cleaned_data['account_type'])
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class ServiceRequestForm(forms.ModelForm):
    
    SERVICES_CHOICES = [
        ('consulting', 'Consulting'),
        ('development', 'Development'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    ]
    
    title = forms.CharField(max_length=100)
    services_needed = forms.MultipleChoiceField(choices=SERVICES_CHOICES, label="Services Needed", widget=forms.CheckboxSelectMultiple)
    location = forms.CharField(max_length=100, label="Location")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    preferable_pricing = forms.DecimalField(max_digits=10, decimal_places=2, label="Preferable Pricing")

    # Optional: To provide placeholder text and other attributes, use the widget attribute
    location = forms.CharField(
        max_length=100, 
        label="Location", 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your location'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe your needs'}),
        label="Description"
    )
    preferable_pricing = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="Preferable Pricing", 
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your preferable pricing'})
    )

    class Meta:
        model = ServiceRequest
        fields = ['title', 'services_needed', 'location', 'description', 'preferable_pricing']
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'Enter your location'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your needs'}),
            'preferable_pricing': forms.NumberInput(attrs={'placeholder': 'Enter your preferable pricing'}),
        }

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['name', 'industry', 'contact_info', 'services', 'previous_works', 'estimated_pricing']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your business name'}),
            'industry': forms.TextInput(attrs={'placeholder': 'Enter your industry'}),
            'contact_info': forms.TextInput(attrs={'placeholder': 'Enter your contact info'}),
            'services': forms.Textarea(attrs={'placeholder': 'Describe your services'}),
            'previous_works': forms.Textarea(attrs={'placeholder': 'Describe your previous works'}),
            'estimated_pricing': forms.NumberInput(attrs={'placeholder': 'Enter your estimated pricing'}),
        }
    
class SearchForServicesOrCompany(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter service or company name'}))

class ReviewForm(forms.ModelForm):
    business_profile = forms.ModelChoiceField(
        queryset=BusinessProfile.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Company'
    )
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '5', 'class': 'form-control'}),
        label='Rating'
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label='Detailed Response'
    )

    class Meta:
        model = Review
        fields = ['business_profile', 'rating', 'comment']
