from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'membership_number', 'membership_type', 'membership_status', 'joined_date']
    list_filter = ['membership_type', 'membership_status', 'is_verified']
    search_fields = ['full_name', 'membership_number', 'email', 'phone_number']
    readonly_fields = ['membership_number', 'joined_date', 'updated_date']
    fieldsets = (
        ('Membership Information', {
            'fields': ('user', 'membership_number', 'membership_type', 'membership_status', 'membership_start_date', 'membership_end_date')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'date_of_birth', 'gender', 'phone_number', 'address', 'city', 'county', 'country')
        }),
        ('Professional Information', {
            'fields': ('occupation', 'organization', 'skills', 'interests')
        }),
        ('Social Media', {
            'fields': ('twitter', 'linkedin', 'facebook', 'instagram'),
            'classes': ('collapse',)
        }),
        ('Additional', {
            'fields': ('profile_pic', 'bio', 'is_verified')
        }),
        ('Tracking', {
            'fields': ('joined_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
