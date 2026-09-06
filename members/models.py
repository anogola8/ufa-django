from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string
from core.models import County, Ward
from core.leadership_positions import ALL_POSITIONS, POSITION_TYPES, get_position_type, get_position_level

class Member(models.Model):
    # Membership Types
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
    
    # Leadership Positions - Using central file
    LEADERSHIP_POSITIONS = ALL_POSITIONS
    
    POSITION_TYPES = [
        ('county', 'County Position'),
        ('ward', 'Ward Position'),
        ('national', 'National Position'),
    ]
    
    # User relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    
    # Membership details
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, default='youth')
    membership_status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS, default='pending')
    membership_number = models.CharField(max_length=20, unique=True, blank=True)
    membership_start_date = models.DateTimeField(default=timezone.now)
    membership_end_date = models.DateTimeField(null=True, blank=True)
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=100, default='Kenya')
    
    # Leadership fields
    leadership_position = models.CharField(max_length=50, choices=LEADERSHIP_POSITIONS, blank=True, null=True)
    position_type = models.CharField(max_length=20, choices=POSITION_TYPES, blank=True, null=True)
    is_leader = models.BooleanField(default=False)
    leadership_level = models.CharField(max_length=50, blank=True, help_text="e.g., County, Ward, National")
    
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
        
        # Auto-set position type and level
        if self.leadership_position:
            self.position_type = get_position_type(self.leadership_position)
            self.leadership_level = get_position_level(self.leadership_position)
            self.is_leader = True
        else:
            self.is_leader = False
            
        super().save(*args, **kwargs)
    
    @property
    def is_active_member(self):
        return self.membership_status == 'active'
