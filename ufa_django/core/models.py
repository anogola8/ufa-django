from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Shared created/updated timestamps. Every substantive model in the
    project should inherit this rather than redeclaring the fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class County(models.Model):
    """Reference data — Kenya's 47 counties. Seeded via a data migration,
    not hardcoded into every app that needs a county choice."""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = 'counties'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ward(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='wards')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['county__name', 'name']
        constraints = [
            models.UniqueConstraint(fields=['county', 'name'], name='unique_ward_per_county'),
        ]

    def __str__(self):
        return f'{self.name}, {self.county.name}'


class SiteSetting(models.Model):
    """Key-value store for site-wide config (contact email, social links,
    org phone, etc.) that shouldn't require a migration to change."""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return self.key


class Document(TimeStampedModel):
    """Shared document repository. Used directly by admins (constitution,
    policies, reports) and can be attached to Articles/Programs once those
    apps exist, without duplicating file-handling logic in each app."""

    class DocumentType(models.TextChoices):
        CONSTITUTION = 'constitution', 'Constitution'
        POLICY = 'policy', 'Policy'
        REPORT = 'report', 'Report'
        OTHER = 'other', 'Other'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/')
    document_type = models.CharField(
        max_length=20, choices=DocumentType.choices, default=DocumentType.OTHER
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='documents'
    )
    is_public = models.BooleanField(
        default=True, help_text='Public documents are downloadable without login.'
    )

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AuditLog(models.Model):
    """Immutable-in-practice log of who did what to which object. Uses a
    generic FK so any app can log against it without core depending on
    events/members/etc. Records are written by a service function, never
    edited or deleted through normal application code."""

    class Action(models.TextChoices):
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'
        APPROVE = 'approve', 'Approve'
        REJECT = 'reject', 'Reject'

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='audit_logs',
    )
    action = models.CharField(max_length=20, choices=Action.choices)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')
    object_repr = models.CharField(max_length=255, blank=True)

    changes = models.JSONField(blank=True, null=True, help_text='Field-level before/after diff, where applicable.')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        who = self.actor or 'system'
        return f'{who} {self.action} {self.object_repr} at {self.timestamp:%Y-%m-%d %H:%M}'
