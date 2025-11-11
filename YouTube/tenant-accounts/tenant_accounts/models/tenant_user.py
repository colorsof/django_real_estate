# apps/tenant_accounts/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
import hashlib, os, uuid
from django.contrib.postgres.fields import ArrayField


class TenantUser(models.Model): 
    """
    Tenant user profile - business logic container.
    Links to GlobalUser for authentication.
    Exists only inside tenant schema.
    """

    USER_TYPES = (
        ('tenant_admin', 'Client Admin/Owner'),
        ('branch_manager', 'Branch Manager'),
        ('loan_officer', 'Loan Officer'),
        ('member', 'Member'),
    )
  
    global_user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
        )


    # Identity details
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

    # Roles and permissions
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    staff_id = models.CharField(max_length=50, unique=True, editable=False)

    # Tenant permissions (assigned by manager)
    allowed_apps = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    allowed_actions = ArrayField(models.CharField(max_length=100), default=list, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    # 🔑 PIN for USSD/app access (KEEP - this is business logic)
    pin_hash = models.CharField(max_length=128, blank=True, null=True)
    pin_salt = models.CharField(max_length=64, blank=True, null=True)
    pin_attempts = models.PositiveIntegerField(default=0)
    pin_locked_until = models.DateTimeField(null=True, blank=True)

    # Login tracking
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=150, null=True, blank=True)


    from tenant_accounts.managers.tenant_user import TenantUserManager
    objects = TenantUserManager()

    class Meta:
        db_table = 'tenant_users'
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['user_type']),
            models.Index(fields=['staff_id']),
            models.Index(fields=['global_user']),  # NEW: For linking queries
        ]

    # --- ID generation (KEEP - business logic) ---
    def _generate_staff_id(self):
        """Generate staff ID with prefix based on role."""
        prefix_map = {
            'tenant_admin': 'TO',
            'branch_manager': 'BM',
            'loan_officer': 'LO',
            'member': 'MB',
        }
        prefix = prefix_map.get(self.user_type, 'U')
        return f"{prefix}-{str(uuid.uuid4()).split('-')[0].upper()}"

    def save(self, *args, **kwargs):
        # Generate staff_id if not exists
        if not self.staff_id:
            self.staff_id = self._generate_staff_id()
            
        # Auto-create/link GlobalUser if needed
        if not self.global_user:
            self.global_user = self._create_or_get_global_user()
            
        self.full_clean()
        super().save(*args, **kwargs)

    # 🔥 NEW: GlobalUser linking logic
    def _create_or_get_global_user(self):
        """Create or get linked GlobalUser"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            # Try to find existing GlobalUser by phone + tenant
            tenant_id = self.get_tenant_id()  # You'll need to implement this
            return User.objects.get(
                phone_number=self.phone_number,
                tenant_id=tenant_id
            )
        except User.DoesNotExist:
            # Create new GlobalUser
            email = self.email or f"{self.phone_number}@tenant{tenant_id}.local"

            if self.user_type in ['tenant_admin', 'branch_manager', 'loan_officer']:
                return User.objects.create_tenant_admin(
                    email=email,
                    phone_number=self.phone_number,
                    tenant_id=tenant_id,
                    tenant_role=self.user_type
                )
            else:
                return User.objects.create_tenant_member(
                    email=email,
                    phone_number=self.phone_number,
                    tenant_id=tenant_id
                )

    def get_tenant_id(self):
        """Get current tenant ID from database connection"""
        from django.db import connection
        return connection.schema_name

    # --- PIN handling (KEEP - business logic) ---
    def set_pin(self, raw_pin: str):
        """Set PIN for tenant user"""
        salt = os.urandom(16)
        self.pin_salt = salt.hex()
        self.pin_hash = hashlib.pbkdf2_hmac("sha256", raw_pin.encode(), salt, 100000).hex()
        self.pin_attempts = 0
        self.pin_locked_until = None
        self.save(update_fields=['pin_hash', 'pin_salt', 'pin_attempts', 'pin_locked_until'])

    def check_pin(self, raw_pin: str) -> bool:
        """Check PIN and handle lockout logic"""
        if self.pin_locked_until and timezone.now() < self.pin_locked_until:
            return False
        if not self.pin_hash or not self.pin_salt:
            return False

        salt = bytes.fromhex(self.pin_salt)
        expected_hash = hashlib.pbkdf2_hmac("sha256", raw_pin.encode(), salt, 100000).hex()
        is_correct = (expected_hash == self.pin_hash)

        if is_correct:
            self.pin_attempts = 0
            self.pin_locked_until = None
        else:
            self.pin_attempts += 1
            if self.pin_attempts >= 3:
                self.pin_locked_until = timezone.now() + timezone.timedelta(minutes=30)

        self.save(update_fields=["pin_attempts", "pin_locked_until"])
        return is_correct

    def is_pin_locked(self) -> bool:
        """Check if PIN is locked due to failed attempts"""
        return self.pin_locked_until and timezone.now() < self.pin_locked_until

    # --- Validation (KEEP) ---
    def clean(self):
        if self.user_type not in dict(self.USER_TYPES):
            raise ValidationError({'user_type': 'Invalid user type'})
        return super().clean()

    # --- Helpers (KEEP + NEW) ---
    @property
    def full_name(self):
        return " ".join([n for n in [self.first_name, self.middle_name, self.last_name] if n])

    @property
    def is_admin_user(self):
        """Check if this is an admin-level user"""
        return self.user_type in ['tenant_admin', 'branch_manager', 'loan_officer']

    @property
    def is_member_user(self):
        """Check if this is a member"""
        return self.user_type == 'member'

    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.user_type in ['tenant_admin', 'branch_manager']

    def can_manage_loans(self):
        """Check if user can manage loans"""
        return self.user_type in ['tenant_admin', 'branch_manager', 'loan_officer']

    def get_authentication_user(self):
        """Get the GlobalUser for Django authentication"""
        return self.global_user

    def __str__(self):
        return f"{self.full_name} ({self.get_user_type_display()})"