ROLE_PERMISSIONS = {
    "tenant_admin": {
        "apps": ["members", "loans", "finance", "tenant_accounts", "branches",  "staff","integrations","reports", "expenses"],
        "actions": ["add", "change", "view", "delete"],
        "custom_perms": [
            "loans.approve_loanapplication",
            "loans.reject_loanapplication",
            "loans.disburse_loanapplication",
            "loans.view_loan_reports",
        ],
        "is_staff": True,
        "is_superuser": False,
    },
    "branch_manager": {
        "apps": ["members", "loans", "finance", "tenant_accounts", "branches"],
        "actions": ["add", "change", "view"],
        "custom_perms": [
            "loans.approve_loanapplication",
            "loans.reject_loanapplication",
            "loans.view_loan_reports",
        ],  # manager can approve/reject but not disburse
        "is_staff": True,
        "is_superuser": False,
    },
    "loan_officer": {
        "apps": ["members", "loans"],
        "actions": ["add", "change", "view"],
        "custom_perms": [
            "loans.view_loan_reports"
        ],  # just process & view reports
        "is_staff": True,
        "is_superuser": False,
    },
    "member": {
        "apps": ["members"],
        "actions": ["view"],
        "custom_perms": [],
        "is_staff": False,
        "is_superuser": False,
    },
}
