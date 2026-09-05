from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Leader(models.Model):
    # NEC POSITIONS
    POSITION_CHOICES = [
        # National Executive Council (NEC)
        ('national_chairperson', 'National Chairperson'),
        ('vice_chairperson_1', 'Vice Chairperson (1st)'),
        ('vice_chairperson_2', 'Vice Chairperson (2nd)'),
        ('secretary_general', 'Secretary General'),
        ('chief_finance_officer', 'Chief Finance Officer'),
        ('national_director_programs', 'National Director of Programs'),
        ('national_youth_leader', 'National Youth Leader'),
        ('empowerment_social_welfare', 'Director of Empowerment & Social Welfare'),
        ('national_women_rep', 'National Women Representative'),
        ('national_organizing_secretary', 'National Organizing Secretary'),
        
        # Other positions
        ('board_member', 'Board Member'),
        ('advisor', 'Advisor'),
        ('other', 'Other'),
    ]
    
    OFFICE_CHOICES = [
        ('sg_office', 'Secretary General\'s Office'),
        ('ceo_office', 'CEO\'s Office'),
        ('vice_chair_1', 'Vice Chair 1 Office'),
        ('vice_chair_2', 'Vice Chair 2 Office'),
        ('cfo_office', 'CFO\'s Office'),
        ('other', 'Other Office'),
    ]
    
    LEADER_TYPES = [
        ('nec', 'National Executive Council (NEC)'),
        ('county', 'County Leader'),
        ('board', 'Board of Directors'),
        ('advisory', 'Advisory Council'),
        ('staff', 'Staff Member'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='other')
    office = models.CharField(max_length=50, choices=OFFICE_CHOICES, default='other')
    leader_type = models.CharField(max_length=20, choices=LEADER_TYPES, default='nec')
    
    # County-specific fields
    county = models.CharField(max_length=100, blank=True, help_text="County name (for county leaders)")
    county_code = models.CharField(max_length=10, blank=True)
    
    # Personal Information
    bio = models.TextField()
    photo = models.ImageField(upload_to='leadership/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Social Media
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    # Additional
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    joined_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['leader_type', 'office', 'order', '-created_at']
        
    def __str__(self):
        if self.leader_type == 'county' and self.county:
            return f"{self.name} - {self.get_position_display()} ({self.county})"
        return f"{self.name} - {self.get_position_display()}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Leader.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
