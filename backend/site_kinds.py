"""Registry of site kinds. Frontage generates three kinds of static sites,
each with its own set of types, its own Jinja template, and its own AI
prompt shape, but sharing the palette system, logo/favicon handling, and
draft persistence.
"""
from business_types import BUSINESS_TYPES
from dashboard_types import DASHBOARD_TYPES
from portfolio_types import PORTFOLIO_TYPES

SITE_KINDS = {
    "business": {
        "label": "Business",
        "description": "Storefront sites for local businesses \u2014 restaurants, clinics, shops.",
        "template": "business.html.jinja",
        "types": BUSINESS_TYPES,
    },
    "portfolio": {
        "label": "Portfolio",
        "description": "Personal sites for developers, designers, and freelancers.",
        "template": "portfolio.html.jinja",
        "types": PORTFOLIO_TYPES,
    },
    "dashboard": {
        "label": "Dashboard",
        "description": "Static product/analytics dashboard mockups with sample data.",
        "template": "dashboard.html.jinja",
        "types": DASHBOARD_TYPES,
    },
}
