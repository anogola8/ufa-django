from django.contrib import admin

from .models import AuditLog, County, Document, SiteSetting, Ward


class WardInline(admin.TabularInline):
    model = Ward
    extra = 1


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name',)
    inlines = [WardInline]


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'county')
    list_filter = ('county',)
    search_fields = ('name', 'county__name')


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')
    search_fields = ('key',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'is_public', 'uploaded_by', 'created_at')
    list_filter = ('document_type', 'is_public')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'content_type', 'object_repr')
    list_filter = ('action', 'content_type')
    search_fields = ('object_repr', 'actor__email')
    readonly_fields = [f.name for f in AuditLog._meta.fields]

    def has_add_permission(self, request):
        # Audit entries are only ever written by application code via
        # core.services.log_action, never created by hand in the admin.
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        # Even super_admins shouldn't be able to erase audit history from
        # the UI. If entries genuinely need pruning (e.g. retention policy),
        # that should be a deliberate management command, not a click.
        return False
