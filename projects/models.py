from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    objective = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    start_date = models.DateField()
    end_date = models.DateField()
    actual_end_date = models.DateField(null=True, blank=True)
    
    location = models.CharField(max_length=200)
    county = models.CharField(max_length=100)
    
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    funding_source = models.CharField(max_length=200, blank=True)
    
    project_lead = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_projects')
    team_members = models.ManyToManyField(User, related_name='projects', blank=True)
    
    featured_image = models.ImageField(upload_to='projects/', blank=True)
    
    beneficiaries = models.PositiveIntegerField(default=0)
    impact_stories = models.TextField(blank=True)
    key_achievements = models.TextField(blank=True)
    
    is_featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        return self.status in ['planning', 'ongoing']

class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published_at']
        
    def __str__(self):
        return f"{self.project.title} - {self.title}"
