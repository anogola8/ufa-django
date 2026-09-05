from django.contrib import admin
from .models import County, Ward, AuditLog

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'code']
    list_filter = ['county']
    search_fields = ['name', 'code']
    ordering = ['county', 'name']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['actor', 'action', 'target', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['actor__username', 'target', 'object_repr']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
