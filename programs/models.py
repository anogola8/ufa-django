from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Program(models.Model):
    PROGRAM_CATEGORIES = [
        ('civic_education', 'Civic Education'),
        ('youth_leadership', 'Youth Leadership'),
        ('advocacy', 'Advocacy'),
        ('community_engagement', 'Community Engagement'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('digital_literacy', 'Digital Literacy'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=PROGRAM_CATEGORIES, default='other')
    description = models.TextField()
    objective = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-graduation-cap', help_text='Font Awesome icon class')
    
    # Program details
    duration = models.CharField(max_length=100, blank=True, help_text='e.g., 3 months, 6 weeks')
    target_audience = models.CharField(max_length=200, blank=True)
    max_participants = models.PositiveIntegerField(default=50)
    
    # Features/Highlights
    features = models.TextField(blank=True, help_text='List program features, one per line')
    requirements = models.TextField(blank=True, help_text='List requirements, one per line')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    # Media
    featured_image = models.ImageField(upload_to='programs/', blank=True)
    
    # Dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Program.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []
    
    def get_requirements_list(self):
        if self.requirements:
            return [r.strip() for r in self.requirements.split('\n') if r.strip()]
        return []
