from django.apps import AppConfig


class TenantAccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tenant_accounts'
    verbose_name = "Tenant Accounts"

