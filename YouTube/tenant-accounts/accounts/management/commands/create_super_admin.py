from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from django.conf import settings
from accounts.models.global_user import GlobalUser
from getpass import getpass
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create a Super Admin in the PUBLIC schema only'

    def handle(self, *args, **options):
        try:
            # ✅ Always use the public schema
            public_schema = getattr(settings, "PUBLIC_SCHEMA_NAME", "public")

            with schema_context(public_schema):
                self.stdout.write(self.style.NOTICE("=== Global Super Admin Details ==="))

                email = self._prompt("Email")
                password = self._get_password()

                # ✅ Prevent duplicates
                if GlobalUser.objects.filter(email=email).exists():
                    self.stdout.write(self.style.ERROR(
                        f"A user with the email '{email}' already exists."
                    ))
                    return

                # ✅ Create GLOBAL super admin
                user = GlobalUser.objects.create_super_admin(
                    email=email,
                    password=password,
                )

                # ✅ Explicitly ensure it's a global user
                # user.client = None
                # user.save(update_fields=["client"])

                self.stdout.write(self.style.SUCCESS(
                    f"✅ Successfully created GLOBAL super admin: {user.email}"
                ))

        except Exception as e:
            logger.exception("Failed to create global super admin")
            self.stderr.write(self.style.ERROR(f"Error: {e}"))

    def _prompt(self, label):
        """Helper to enforce required input."""
        value = input(f"{label}: ").strip()
        while not value:
            print("⚠️ This field is required.")
            value = input(f"{label}: ").strip()
        return value

    def _get_password(self):
        """Prompt until a valid password + confirmation is entered."""
        while True:
            password = getpass("Password: ")
            confirm = getpass("Confirm password: ")
            if not password:
                print("⚠️ Password cannot be empty.")
            elif password != confirm:
                print("⚠️ Passwords do not match. Please try again.")
            else:
                return password   # ✅ return string only
