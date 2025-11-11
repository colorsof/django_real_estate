from django.db import models, transaction
from django.contrib.auth.models import BaseUserManager
import logging

logger = logging.getLogger(__name__)

class GlobalUserManager(BaseUserManager):
    """Manager for GlobalUser (super admins / platform staff / tenant-linked users)"""

    @transaction.atomic
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a normal global user"""
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        logger.info(f"Created GlobalUser: {user.email} ({extra_fields.get('user_type')})")
        return user

    @transaction.atomic
    def create_super_admin(self, email, password=None, **extra_fields):
        """Create a platform-level super admin"""
        extra_fields.setdefault("user_type", "super_admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email=email, password=password, **extra_fields)

    @transaction.atomic
    def create_platform_staff(self, email, password=None, **extra_fields):
        """Create a platform staff user (not superuser)"""
        extra_fields.setdefault("user_type", "platform_staff")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email=email, password=password, **extra_fields)

    # 🔥 FIX: Updated method names to match your GlobalUser model
    @transaction.atomic
    def create_tenant_admin(self, email, phone_number, tenant_id, tenant_role=None, password=None, **extra_fields):
        """Create a GlobalUser for tenant admin (owner, branch manager, loan officer)"""
        extra_fields.setdefault("user_type", "tenant_admin")
        extra_fields.setdefault("phone_number", phone_number)
        extra_fields.setdefault("tenant_id", tenant_id)
        extra_fields.setdefault("tenant_role", tenant_role)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(email=email, password=password, **extra_fields)

    @transaction.atomic
    def create_tenant_member(self, email, phone_number, tenant_id, password=None, **extra_fields):
        """Create a GlobalUser for tenant member"""
        extra_fields.setdefault("user_type", "tenant_member")
        extra_fields.setdefault("phone_number", phone_number)
        extra_fields.setdefault("tenant_id", tenant_id)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(email=email, password=password, **extra_fields)

    # 🔥 REMOVED: create_tenant_linked_user (doesn't match your model's USER_TYPES)