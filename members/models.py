from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class Member(models.Model):
    MEMBERSHIP_TYPES = [
        ('individual', 'Individual Member'),
        ('student', 'Student Member'),
        ('youth', 'Youth Member'),
        ('senior', 'Senior Member'),
        ('lifetime', 'Lifetime Member'),
        ('organizational', 'Organizational Member'),
    ]
    
    MEMBERSHIP_STATUS = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, default='youth')
    membership_status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS, default='pending')
    membership_number = models.CharField(max_length=20, unique=True, blank=True)
    membership_start_date = models.DateTimeField(default=timezone.now)
    membership_end_date = models.DateTimeField(null=True, blank=True)
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Kenya')
    
    # Professional Information
    occupation = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    
    # Social Media
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    # Additional
    profile_pic = models.ImageField(upload_to='members/', default='members/default.jpg')
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-joined_date']
        
    def __str__(self):
        return f"{self.full_name} ({self.membership_number})"
    
    def save(self, *args, **kwargs):
        if not self.membership_number:
            self.membership_number = ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)
    
    @property
    def is_active_member(self):
        return self.membership_status == 'active'
