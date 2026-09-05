from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from members.models import Member
from leadership.models import Leader

class Appointment(models.Model):
    POSITION_CHOICES = [
        ('county_chairperson', 'County Chairperson'),
        ('county_vice_chairperson', 'County Vice Chairperson'),
        ('county_secretary', 'County Secretary'),
        ('county_treasurer', 'County Treasurer'),
        ('ward_leader', 'Ward Leader'),
        ('national_official', 'National Official'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    ISSUER_CHOICES = [
        ('chairperson', 'National Chairperson'),
        ('vice_chair_1', '1st Vice Chairperson'),
        ('vice_chair_2', '2nd Vice Chairperson'),
        ('secretary_general', 'Secretary General'),
        ('other', 'Other'),
    ]
    
    # Member being appointed
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='appointments')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    county = models.CharField(max_length=100, blank=True, help_text="County for county positions")
    ward = models.CharField(max_length=100, blank=True, help_text="Ward for ward positions")
    
    # Appointment details
    appointment_date = models.DateField(default=timezone.now)
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
    # Issuer information (Office of Vice Chair II)
    issuer = models.CharField(max_length=50, choices=ISSUER_CHOICES, default='vice_chair_2')
    issuer_name = models.CharField(max_length=200, blank=True, default='Dericks Omondi', help_text="Name of the person issuing the letter")
    issuer_title = models.CharField(max_length=200, blank=True, default='2nd Vice Chairperson - Appointments', help_text="Title of the issuer")
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_appointments')
    approved_date = models.DateTimeField(null=True, blank=True)
    
    # Letter details
    letter_reference = models.CharField(max_length=50, unique=True, blank=True)
    letter_content = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='appointments/letters/', blank=True, null=True)
    
    # Additional notes
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.member.full_name} - {self.get_position_display()}"
    
    def save(self, *args, **kwargs):
        if not self.letter_reference:
            import datetime
            year = datetime.datetime.now().year
            count = Appointment.objects.filter(created_at__year=year).count() + 1
            self.letter_reference = f"UFA/APP/{year}/{str(count).zfill(3)}"
        
        # Set default issuer name and title for Office of Vice Chair II
        if not self.issuer_name:
            self.issuer_name = "Dericks Omondi"
        if not self.issuer_title:
            self.issuer_title = "2nd Vice Chairperson - Appointments"
            
        super().save(*args, **kwargs)
