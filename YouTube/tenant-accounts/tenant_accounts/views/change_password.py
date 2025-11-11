# apps/accounts/views/change_password.py
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from tenant_accounts.forms.change_password import ChangePasswordForm

from django_tenants.utils import schema_context

class ChangePasswordView(LoginRequiredMixin, View):
    template_name = "tenants/admin_profile.html"

    def get(self, request):
        form = ChangePasswordForm(request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            with schema_context("public"):  # 👈 make sure we're updating GlobalUser
                user = request.user
                user.set_password(form.cleaned_data["new_password"])
                user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully ✅")
            return redirect("dashboard:home")
        return render(request, self.template_name, {"form": form})
