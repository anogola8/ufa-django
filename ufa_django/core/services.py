"""
Shared service functions. Keeping this logic out of views/models means
every app writes audit entries the same way instead of reinventing it.
"""
from django.contrib.contenttypes.models import ContentType

from core.models import AuditLog


def log_action(*, actor, action, target=None, changes=None, ip_address=None, object_repr=''):
    """Write one AuditLog row.

    `target` is any model instance (e.g. a Membership being approved).
    `changes` should be a small JSON-serializable dict of before/after
    values — don't dump entire model __dict__s here, just the fields that
    actually changed, so the log stays readable and doesn't leak fields
    that shouldn't be logged (password hashes, tokens).
    """
    content_type = None
    object_id = None
    if target is not None:
        content_type = ContentType.objects.get_for_model(target)
        object_id = target.pk
        object_repr = object_repr or str(target)

    return AuditLog.objects.create(
        actor=actor,
        action=action,
        content_type=content_type,
        object_id=object_id,
        object_repr=object_repr,
        changes=changes,
        ip_address=ip_address,
    )
