from tenant_accounts.views.admin_profile import admin_profile
from django.urls import path
from tenant_accounts.views.change_password import ChangePasswordView

app_name = 'accounts'


urlpatterns = [
    path('profile/', admin_profile, name='profile'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),

]
