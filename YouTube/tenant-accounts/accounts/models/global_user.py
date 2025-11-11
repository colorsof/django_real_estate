# apps/accounts/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
import logging

logger = logging.getLogger(__name__)


class GlobalUser(AbstractBaseUser, PermissionsMixin):
    """
    Single AUTH_USER_MODEL for all authentication.
    Handles both global admins and tenant users.
    """
    USER_TYPES = (
        ("super_admin", "Super Admin"),
        ("platform_staff", "Platform Staff"),
        ("tenant_admin", "Tenant Admin"),        # NEW: Owner, Branch Manager, Loan Officer
        ("tenant_member", "Tenant Member"),      # NEW: Basic Members
    )

    # Core Identity (for all users)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="platform_staff")

    # Global Admin Flags (only for super_admin/platform_staff)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)     # Changed default to False
    is_superuser = models.BooleanField(default=False)

    # Tenant User Fields (only for tenant_admin/tenant_member)
    tenant_id = models.CharField(max_length=100, blank=True, null=True, 
                                help_text="Tenant identifier for tenant users")
    phone_number = models.CharField(max_length=15, blank=True, null=True,
                                   help_text="Phone number for tenant user authentication")
    tenant_role = models.CharField(max_length=20, blank=True, null=True,
                                  help_text="Specific role: owner, branch_manager, loan_officer, member")
    is_phone_verified = models.BooleanField(default=False,null=True, blank=True)
    is_email_verified = models.BooleanField(default=False,null=True, blank=True)

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Manager
    from accounts.managers.global_user import GlobalUserManager
    objects = GlobalUserManager()

    class Meta:
        db_table = "global_users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["user_type"]),
            models.Index(fields=["tenant_id"]),           # NEW: For tenant user queries
            models.Index(fields=["phone_number"]),        # NEW: For phone-based auth
        ]
        constraints = [
            # Ensure phone_number is unique per tenant (not globally unique)
            models.UniqueConstraint(
                fields=['phone_number', 'tenant_id'],
                condition=models.Q(tenant_id__isnull=False),
                name='unique_phone_per_tenant'
            ),
            # Ensure tenant users have required fields
            models.CheckConstraint(
                check=models.Q(
                    user_type__in=['super_admin', 'platform_staff']
                ) | models.Q(
                    user_type__in=['tenant_admin', 'tenant_member'],
                    tenant_id__isnull=False,
                    phone_number__isnull=False
                ),
                name='tenant_users_have_required_fields'
            )
        ]

    def save(self, *args, **kwargs):
        """Ensure flags and fields match user type before saving"""
        if self.user_type == "super_admin":
            self.is_superuser = True
            self.is_staff = True
            # Clear tenant fields for global users
            self.tenant_id = None
            self.phone_number = None
            self.tenant_role = None
            
        elif self.user_type == "platform_staff":
            self.is_superuser = False
            self.is_staff = True
            # Clear tenant fields for global users
            self.tenant_id = None
            self.phone_number = None
            self.tenant_role = None
            
        elif self.user_type == "tenant_admin":
            self.is_superuser = False
            self.is_staff = True
            # Tenant users must have tenant_id and phone_number
            if not self.tenant_id or not self.phone_number:
                raise ValueError(f"Tenant users must have tenant_id and phone_number")
            
        elif self.user_type == "tenant_member":
            self.is_superuser = False
            self.is_staff = False
            # Tenant users must have tenant_id and phone_number
            if not self.tenant_id or not self.phone_number:
                raise ValueError(f"Tenant users must have tenant_id and phone_number")
            
      
        super().save(*args, **kwargs)

    # =====================================
    # PROPERTIES & HELPER METHODS
    # =====================================
    @property
    def is_global_user(self):
        """Check if this is a global admin user"""
        return self.user_type in ['super_admin', 'platform_staff']

    @property
    def is_tenant_user(self):
        """Check if this is a tenant user"""
        return self.user_type in ['tenant_admin', 'tenant_member']

    @property
    def is_tenant_admin_user(self):
        """Check if this is a tenant admin (owner, branch manager, loan officer)"""
        return self.user_type == 'tenant_admin'

    @property
    def is_tenant_member_user(self):
        """Check if this is a tenant member"""
        return self.user_type == 'tenant_member'

    def get_tenant_profile(self):
        """
        Safely return the linked TenantUser profile.
        Works only inside a tenant schema.
        """
        if not self.is_tenant_user:
            return None

        from django.db import connection
        if connection.schema_name == "public":
            # Prevent errors when called in super admin
            return None

        try:
            return self.tenant_profile
        except Exception:
            return None


    def can_manage_tenant(self, tenant_id):
        """Check if user can manage specific tenant"""
        if self.is_global_user:
            return True  # Global users can manage all tenants
        return self.tenant_id == tenant_id

    def __str__(self):
        if self.is_global_user:
            return f"{self.email} ({self.get_user_type_display()})"
        else:
            return f"{self.email} - {self.phone_number} ({self.get_user_type_display()})"

    # =====================================
    # AUTHENTICATION HELPERS
    # =====================================
    def uses_password_auth(self):
        """Check if user uses password authentication"""
        return self.user_type in ['super_admin', 'platform_staff']

    def uses_pin_auth(self):
        """Check if user uses PIN authentication"""
        return self.user_type in ['tenant_admin', 'tenant_member']