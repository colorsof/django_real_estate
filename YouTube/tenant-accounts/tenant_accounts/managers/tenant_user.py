from django.db import models, transaction, connection
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import logging
from tenant_accounts.permissions.role_permissions import ROLE_PERMISSIONS
from django.contrib.auth.models import Permission
from django.apps import apps
from django_tenants.utils import get_public_schema_name, schema_context
from django.db import connection
from django.db import IntegrityError, transaction

logger = logging.getLogger(__name__)

User = get_user_model()
class TenantUserManager(models.Manager):
    """Manager for tenant-level user profiles"""

    # -----------------------
    # Public entry points
    # -----------------------
    @transaction.atomic
    def create_owner(self, first_name, last_name, phone_number, email=None, password=None, **extra_fields):
        return self._create_tenant_user(
            user_type="tenant_admin",
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password,
            **extra_fields
        )

    @transaction.atomic
    def create_branch_manager(self, first_name, last_name, phone_number, email=None, password=None, **extra_fields):
        return self._create_tenant_user(
            user_type="branch_manager",
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password,
            **extra_fields
        )

    @transaction.atomic
    def create_loan_officer(self, first_name, last_name, phone_number, email=None, password=None, **extra_fields):
        return self._create_tenant_user(
            user_type="loan_officer",
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password,
            **extra_fields
        )

    @transaction.atomic
    def create_member(self, first_name, last_name, phone_number, email=None, password=None, raw_pin=None, **extra_fields):
        tenant_user = self._create_tenant_user(
            user_type="member",
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password,
            **extra_fields
        )

        # Set PIN if provided
        if raw_pin:
            tenant_user.set_pin(raw_pin)
            tenant_user.save(update_fields=["pin_hash", "pin_salt", "pin_attempts", "pin_locked_until"])

        # Create Member profile extension
        from members.models import Member
        member = Member.objects.create(
            tenant_user=tenant_user,
            branch=extra_fields.get("branch"),
            credit_score=extra_fields.get("credit_score", 0),
            account_balance=extra_fields.get("account_balance", 0.00),
            loan_limit=extra_fields.get("loan_limit", 0.00),
            CRB_status=extra_fields.get("CRB_status"),
        )

        return member

    # -----------------------
    # Core Creation Logic
    # -----------------------
    def _create_tenant_user(self, user_type, first_name, last_name, phone_number, email=None, password=None, **extra_fields):
        tenant_id = self._get_current_tenant_id()

        # Generate email if not provided
        if not email:
            email = f"{first_name}.{last_name}@{tenant_id}.com".lower()

        # Get or create GlobalUser
        global_user = self._get_or_create_global_user(
            email=email,
            phone_number=phone_number,
            tenant_id=tenant_id,
            user_type=user_type,
            password=password,
        )

        # Create TenantUser profile
        tenant_user = self.model(
            global_user=global_user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            user_type=user_type,
            **extra_fields,
        )
        tenant_user.save(using=self._db)

        # Assign permissions
        self._assign_permissions(tenant_user)

        logger.info(f"Tenant user created: {tenant_user.full_name} ({user_type}) in tenant={tenant_id}")
        return tenant_user



    def _get_or_create_global_user(self, email, phone_number, tenant_id, user_type, password=None):
        """
        Always create or get GlobalUser in the PUBLIC schema.
        Ensures one GlobalUser per (phone_number, tenant_id).
        """
        User = get_user_model()

        with schema_context(get_public_schema_name()):
            try:
                # Try to find by phone+tenant first
                return User.objects.get(phone_number=phone_number, tenant_id=tenant_id)
            except User.DoesNotExist:
                pass

            try:
                # Try to find by email (update tenant if needed)
                global_user = User.objects.get(email=email)
                global_user.phone_number = phone_number
                global_user.tenant_id = tenant_id
                if user_type in ['tenant_admin', 'branch_manager', 'loan_officer']:
                    global_user.user_type = 'tenant_admin'
                    global_user.tenant_role = user_type
                else:
                    global_user.user_type = 'tenant_member'
                global_user.save()
                return global_user
            except User.DoesNotExist:
                pass

            # Force-create new GlobalUser
            try:
                with transaction.atomic():
                    if user_type in ['tenant_admin', 'branch_manager', 'loan_officer']:
                        global_user = User.objects.create_tenant_admin(
                            email=email,
                            phone_number=phone_number,
                            tenant_id=tenant_id,
                            tenant_role=user_type,
                            password=password,
                        )
                    else:
                        global_user = User.objects.create_tenant_member(
                            email=email,
                            phone_number=phone_number,
                            tenant_id=tenant_id,
                            password=password,
                        )
                    logger.info(f"Created GlobalUser in public schema: {phone_number} ({user_type})")
                    return global_user
            except IntegrityError as e:
                logger.error(f"IntegrityError while creating GlobalUser: {e}")
                raise ValueError(f"Failed to create GlobalUser for {phone_number} in {tenant_id}")


    def _assign_permissions(self, tenant_user):
        """
        Assign tenant-level allowed_apps/allowed_actions to TenantUser
        and sync necessary permissions to the linked GlobalUser so the
        user can see/manage models in Django admin.
        """
        role = tenant_user.user_type
        if role not in ROLE_PERMISSIONS:
            return []

        role_config = ROLE_PERMISSIONS[role]

        # Save allowed apps/actions inside TenantUser (business logic)
        tenant_user.allowed_apps = role_config.get("apps", [])
        tenant_user.allowed_actions = role_config.get("actions", [])
        tenant_user.save(update_fields=["allowed_apps", "allowed_actions"])

        # Sync staff/superuser flags to GlobalUser
        global_user = tenant_user.global_user
        global_user.is_staff = role_config.get("is_staff", False)
        global_user.is_superuser = role_config.get("is_superuser", False)
        global_user.save(update_fields=["is_staff", "is_superuser"])

        # If global user is platform superuser, don't touch permissions (they already have access)
        if global_user.is_superuser:
            logger.debug(f"GlobalUser {global_user.pk} is superuser; skipping permission assignment.")
            return tenant_user.allowed_apps

        # Build list of permission strings: custom perms + CRUD perms for allowed apps
        perms = list(role_config.get("custom_perms", []))

        # Add CRUD perms for each model in allowed apps (e.g., "members.view_member")
        for app_label in tenant_user.allowed_apps:
            try:
                app_config = apps.get_app_config(app_label)
            except LookupError:
                logger.warning(f"App '{app_label}' not found while assigning permissions for tenant {self._get_current_tenant_id()}")
                continue

            for model in app_config.get_models():
                model_name = model._meta.model_name
                for action in tenant_user.allowed_actions:
                    # action is like 'view', 'add', 'change', 'delete'
                    perms.append(f"{app_label}.{action}_{model_name}")

        # Extract codenames from permission strings and fetch Permission objects
        codenames = [p.split(".")[-1] for p in perms]
        perm_objs = Permission.objects.filter(codename__in=codenames)

        # Option A (recommended for most cases): replace user's permissions for tenant role
        # This ensures they only have the permissions defined by the role.
        # Be careful: this will remove any other user_permissions previously set.
        global_user.user_permissions.set(perm_objs)

        # If instead you prefer to *add* the tenant perms and keep existing platform perms, use:
        # global_user.user_permissions.add(*perm_objs)

        logger.info(f"Assigned {len(perm_objs)} permissions to GlobalUser {global_user.pk} for role {role}")
        return tenant_user.allowed_apps

    def _get_current_tenant_id(self):
        """Return the current schema/tenant id"""
        return connection.schema_name
