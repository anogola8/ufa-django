from django.contrib import admin
from .models import Leader

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'leader_type', 'county', 'is_active', 'is_featured', 'order')
    list_filter = ('leader_type', 'position', 'is_active', 'is_featured', 'county')
    search_fields = ('name', 'position', 'county', 'email', 'phone')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('leader_type', 'order', 'name')
    fieldsets = (
        ('Member Information', {
            'fields': ('name', 'slug', 'position', 'leader_type', 'county', 'county_code')
        }),
        ('Personal Information', {
            'fields': ('bio', 'photo', 'email', 'phone')
        }),
        ('Social Media', {
            'fields': ('twitter', 'linkedin', 'facebook', 'instagram'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_featured', 'order', 'joined_date')
        }),
    )
