"""Static configuration for each supported business type.

Adding a new type only requires a new entry here, no new template file.
`fallback_copy` is used when no ANTHROPIC_API_KEY is configured, so the tool
still produces a usable (if generic) preview.

`schema_type` maps to a schema.org type used in the exported site's JSON-LD
structured data (helps local SEO / Google Business-style search results).
"""

BUSINESS_TYPES = {
    "restaurant": {
        "label": "Restaurant / Food",
        "layout": "grid",
        "schema_type": "Restaurant",
        "highlight_section_label": "What we're known for",
        "highlight_count": 4,
        "contact_heading": "Ready to order?",
        "contact_subtext": "Message us on WhatsApp and we'll take it from there.",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M7 3v7a2 2 0 0 0 2 2 2 2 0 0 0 2-2V3M9 12v9"/>'
            '<path d="M16 3c-1.5 0-3 1.6-3 4.5S14.5 12 16 12s3-1.6 3-4.5S17.5 3 16 3z"/>'
            '<path d="M16 12v9"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Real Food, Made Fresh Daily",
            "tagline": "Homestyle cooking, generous portions, and fast WhatsApp ordering.",
            "about": (
                "We've been serving the neighbourhood with fresh, made-to-order food. "
                "Every dish is prepared with care using quality ingredients, and we keep "
                "our menu simple so we can do it well."
            ),
            "cta_text": "Order on WhatsApp",
            "highlights": [
                {"title": "Made Fresh Daily", "description": "Nothing sits around - everything is cooked to order."},
                {"title": "Fast Delivery", "description": "Quick turnaround across the local area."},
                {"title": "Family Recipes", "description": "Recipes passed down and perfected over time."},
                {"title": "Easy Ordering", "description": "Order in seconds, right from WhatsApp."},
            ],
        },
    },
    "medical": {
        "label": "Medical Store / Pharmacy",
        "layout": "list",
        "schema_type": "Pharmacy",
        "highlight_section_label": "How we help",
        "highlight_count": 4,
        "contact_heading": "Need something today?",
        "contact_subtext": "Message us on WhatsApp - we'll confirm availability and delivery.",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<circle cx="12" cy="12" r="9"/><path d="M12 7.5v9M7.5 12h9"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Your Neighbourhood Pharmacy",
            "tagline": "Genuine medicines, fast delivery, and a team you can trust.",
            "about": (
                "We stock a wide range of medicines and healthcare essentials, and we're "
                "just a WhatsApp message away for anything you need. Our priority is "
                "getting you the right product, quickly and reliably."
            ),
            "cta_text": "Message on WhatsApp",
            "highlights": [
                {"title": "Genuine Medicines", "description": "Sourced from trusted suppliers only."},
                {"title": "Same-Day Delivery", "description": "Order today, delivered close to home."},
                {"title": "Easy Reordering", "description": "Send a photo of your prescription on WhatsApp."},
                {"title": "Friendly Advice", "description": "Our staff are happy to help you choose."},
            ],
        },
    },
    "dentist": {
        "label": "Dentist / Dental Clinic",
        "layout": "list",
        "schema_type": "Dentist",
        "highlight_section_label": "Our services",
        "highlight_count": 4,
        "contact_heading": "Ready to book?",
        "contact_subtext": "Message us on WhatsApp to schedule your visit.",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M12 3c-2.4 0-4.4 1.5-4.4 4 0 1.9-.5 2.9-.9 4.7-.4 1.7-.2 3.9.9 5.7 '
            '.6.9 1.4.9 1.9-.5.4-1.2.7-2.9 2.5-2.9s2.1 1.7 2.5 2.9c.5 1.4 1.3 1.4 1.9.5 '
            '1.1-1.8 1.3-4 .9-5.7-.4-1.8-.9-2.8-.9-4.7 0-2.5-2-4-4.4-4z"/></svg>'
        ),
        "fallback_copy": {
            "headline": "A Healthier Smile Starts Here",
            "tagline": "Gentle, modern dental care for the whole family.",
            "about": (
                "From routine checkups to more involved treatments, we focus on making "
                "every visit comfortable. Our clinic combines modern equipment with a "
                "friendly, patient approach."
            ),
            "cta_text": "Book on WhatsApp",
            "highlights": [
                {"title": "General Checkups", "description": "Regular cleanings and preventive care."},
                {"title": "Painless Procedures", "description": "Modern techniques focused on comfort."},
                {"title": "Flexible Timings", "description": "Evening and weekend slots available."},
                {"title": "Easy Booking", "description": "Book your appointment over WhatsApp."},
            ],
        },
    },
    "services": {
        "label": "General Services",
        "layout": "list",
        "schema_type": "LocalBusiness",
        "highlight_section_label": "What we offer",
        "highlight_count": 4,
        "contact_heading": "Have a project in mind?",
        "contact_subtext": "Message us on WhatsApp for a free quote.",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2-2z"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Reliable Help, When You Need It",
            "tagline": "Straightforward, quality work - no surprises.",
            "about": (
                "We take on jobs big and small, and we treat every client's home or "
                "project like our own. Clear communication, fair pricing, and work you "
                "can count on."
            ),
            "cta_text": "Get a Free Quote",
            "highlights": [
                {"title": "Free Estimates", "description": "No obligation quote before we start."},
                {"title": "On-Time Work", "description": "We show up when we say we will."},
                {"title": "Fair Pricing", "description": "Transparent costs, no hidden fees."},
                {"title": "Local & Trusted", "description": "Based nearby, with references available."},
            ],
        },
    },
    "salon": {
        "label": "Salon / Beauty",
        "layout": "grid",
        "schema_type": "BeautySalon",
        "highlight_section_label": "Popular services",
        "highlight_count": 4,
        "contact_heading": "Ready for a fresh look?",
        "contact_subtext": "Message us on WhatsApp to book your slot.",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M6 4c3 2 4 5 4 8s-1 6-4 8"/><path d="M18 4c-3 2-4 5-4 8s1 6 4 8"/>'
            '<circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Look Good, Feel Better",
            "tagline": "Skilled stylists, a relaxed space, and appointments that run on time.",
            "about": (
                "Whether it's a quick trim or a full makeover, we take the time to get it "
                "right. Our team stays current with trends while keeping the experience "
                "comfortable and unhurried."
            ),
            "cta_text": "Book on WhatsApp",
            "highlights": [
                {"title": "Hair Styling", "description": "Cuts, color, and styling for every occasion."},
                {"title": "Skin & Facial Care", "description": "Treatments tailored to your skin type."},
                {"title": "Bridal Packages", "description": "Full bridal and party makeup packages."},
                {"title": "Easy Booking", "description": "Reserve your slot over WhatsApp."},
            ],
        },
    },
    "retail": {
        "label": "Retail / Shop",
        "layout": "grid",
        "schema_type": "Store",
        "highlight_section_label": "Why shop with us",
        "highlight_count": 4,
        "contact_heading": "Looking for something specific?",
        "contact_subtext": "Message us on WhatsApp - we'll check what's in stock.",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M4 8l1.5-4h13L20 8"/><path d="M4 8h16v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V8z"/>'
            '<path d="M9 12a3 3 0 0 0 6 0"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Quality You Can Count On",
            "tagline": "A carefully chosen selection, fair prices, and friendly service.",
            "about": (
                "We stock a range of quality products and update it regularly based on "
                "what our customers ask for. Come by or message us - we're happy to help "
                "you find exactly what you need."
            ),
            "cta_text": "Message on WhatsApp",
            "highlights": [
                {"title": "Quality Checked", "description": "Every item is inspected before it hits the shelf."},
                {"title": "Fair Prices", "description": "Honest pricing, no bargaining games."},
                {"title": "New Arrivals Weekly", "description": "Fresh stock added regularly."},
                {"title": "Easy Ordering", "description": "Ask about anything over WhatsApp."},
            ],
        },
    },
    "real-estate": {
        "label": "Real Estate / Property",
        "layout": "list",
        "schema_type": "RealEstateAgent",
        "highlight_section_label": "What we handle",
        "highlight_count": 4,
        "contact_heading": "Looking to buy, sell, or rent?",
        "contact_subtext": "Message us on WhatsApp with what you're looking for.",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M4 11l8-7 8 7"/><path d="M6 10v9a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-9"/>'
            '<path d="M10 20v-6h4v6"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Find Your Next Property",
            "tagline": "Honest advice on buying, selling, and renting - no pressure.",
            "about": (
                "We help families and investors find the right property, and help owners "
                "get a fair deal when selling or renting. Every listing is verified before "
                "it goes out to clients."
            ),
            "cta_text": "Message on WhatsApp",
            "highlights": [
                {"title": "Verified Listings", "description": "Every property is checked before we show it."},
                {"title": "Buying & Selling", "description": "Guidance through the full process."},
                {"title": "Rentals", "description": "Residential and commercial rental options."},
                {"title": "Local Expertise", "description": "Deep knowledge of the area's market."},
            ],
        },
    },
    "education": {
        "label": "Education / Academy",
        "layout": "list",
        "schema_type": "EducationalOrganization",
        "highlight_section_label": "What we offer",
        "highlight_count": 4,
        "contact_heading": "Ready to enroll?",
        "contact_subtext": "Message us on WhatsApp for class timings and fees.",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M2 9l10-5 10 5-10 5-10-5z"/><path d="M6 11.5V17c0 1.5 3 3 6 3s6-1.5 6-3v-5.5"/>'
            '<path d="M22 9v6"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Learning That Actually Sticks",
            "tagline": "Small classes, dedicated teachers, and real progress you can see.",
            "about": (
                "We focus on understanding, not just memorizing - with small class sizes "
                "so every student gets real attention. Regular progress updates keep "
                "parents in the loop too."
            ),
            "cta_text": "Message on WhatsApp",
            "highlights": [
                {"title": "Small Class Sizes", "description": "More attention for every student."},
                {"title": "Experienced Teachers", "description": "Qualified instructors who care about results."},
                {"title": "Regular Progress Reports", "description": "Parents stay updated throughout."},
                {"title": "Flexible Timings", "description": "Morning, evening, and weekend batches."},
            ],
        },
    },
}
