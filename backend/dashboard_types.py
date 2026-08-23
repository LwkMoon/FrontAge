"""Static configuration for each supported dashboard type.

Dashboards are UI mockups, not marketing pages: nav items and stat labels
are the person's own input (or the defaults below), and the stat *values*
shown in the export are deterministic sample data generated from those
labels, never AI-invented or claimed as real. See services/demo_data.py.
"""

DASHBOARD_TYPES = {
    "saas-analytics": {
        "label": "SaaS Analytics",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/></svg>'
        ),
        "default_nav_items": "Overview, Analytics, Customers, Revenue, Settings",
        "default_stat_labels": "MRR, Active Users, Conversion Rate, Churn Rate",
        "fallback_copy": {
            "headline": "Your growth, at a glance",
            "tagline": "Every metric that matters, in one screen.",
            "welcome_message": "Here's what's happening with your product today.",
            "cta_text": "View Report",
        },
    },
    "admin-panel": {
        "label": "Admin Panel",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<circle cx="12" cy="12" r="3"/>'
            '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15 1.65 1.65 0 0 0 3.17 14H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
        ),
        "default_nav_items": "Dashboard, Users, Roles, Logs, Settings",
        "default_stat_labels": "Total Users, Open Tickets, Uptime, Storage Used",
        "fallback_copy": {
            "headline": "Everything running smoothly",
            "tagline": "One place to manage users, permissions, and system health.",
            "welcome_message": "Here's a quick look at your system today.",
            "cta_text": "View Logs",
        },
    },
    "ecommerce": {
        "label": "E-commerce Dashboard",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<circle cx="9" cy="21" r="1"/><circle cx="19" cy="21" r="1"/>'
            '<path d="M2.5 3h2l2.7 12.4a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.6L21 7H6"/></svg>'
        ),
        "default_nav_items": "Overview, Orders, Products, Customers, Settings",
        "default_stat_labels": "Total Sales, Orders Today, Avg Order Value, Returns",
        "fallback_copy": {
            "headline": "Your store, at a glance",
            "tagline": "Sales, orders, and customers in one screen.",
            "welcome_message": "Here's how the store is doing today.",
            "cta_text": "View Orders",
        },
    },
}
