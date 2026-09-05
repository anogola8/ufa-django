from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import County, Ward


class UserManager(BaseUserManager):
    """Custom manager required because we use email, not username, as the
    login field — Django's default UserManager assumes `username`."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.SUPER_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user: email is the login identifier, `username` is dropped.

    `role` is a fast-path field for simple checks (is_admin() etc). It is
    NOT the enforcement mechanism for permissions — real access control
    should go through Django's Groups/Permissions, with `role` used at
    signup/promotion time to assign the right group. See the architecture
    doc for the reasoning.
    """

    class Role(models.TextChoices):
        MEMBER = 'member', 'Member'
        STAFF = 'staff', 'Staff'
        ADMIN = 'admin', 'Admin'
        SUPER_ADMIN = 'super_admin', 'Super Admin'

    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True, related_name='residents')
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name='residents')

    # MFA-ready fields (Phase 8 requirement). TOTP enrollment/verification
    # flow is not implemented yet — these fields let the data model support
    # it without a later migration. mfa_secret should be encrypted at rest
    # once a real KMS/encryption-at-rest solution is chosen for deployment.
    is_mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=255, blank=True)

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} <{self.email}>'

    @property
    def is_admin(self):
        return self.role in {self.Role.ADMIN, self.Role.SUPER_ADMIN} or self.is_superuser

    @property
    def is_staff_or_above(self):
        return self.role in {self.Role.STAFF, self.Role.ADMIN, self.Role.SUPER_ADMIN} or self.is_superuser
