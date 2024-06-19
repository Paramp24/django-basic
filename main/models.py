# models.py
from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    
    SERVICES_CHOICES = [
        ('consulting', 'Consulting'),
        ('development', 'Development'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_requests', default=1)
    title = models.CharField(max_length=100, default='Default Title')
    services_needed = models.CharField(max_length=200)  # Store as a comma-separated string
    location = models.CharField(max_length=100)
    description = models.TextField()
    preferable_pricing = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.title} - {self.services_needed}"
     
class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    services = models.TextField()
    previous_works = models.TextField()
    estimated_pricing = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=[('individual', 'Individual'), ('business', 'Business')])

    def __str__(self):
        return self.user.username

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    BusinessProfile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.BusinessProfile.name}'
