def map_audit_to_scores(audit_results: dict) -> dict:
    """
    Converts raw collector outputs into 0–100 section scores
    (UNIVERSAL: works for local businesses, agencies, SaaS)
    """

    business = audit_results.get("business_info", {})
    tech = audit_results.get("tech_stack", {})
    pagespeed = audit_results.get("pagespeed", {})
    google = audit_results.get("google_reviews", {})
    facebook = audit_results.get("facebook_reviews", {})
    seo = audit_results.get("seo_visibility", {})

    # --------------------------------------------------
    # BUSINESS DETAILS (Contact + Address + Phone)
    # --------------------------------------------------
    business_score = 0
    if business.get("business_name"):
        business_score += 30
    if business.get("phones"):
        business_score += 30
    if business.get("address"):
        business_score += 20
    if business.get("contact_page"):
        business_score += 20

    business_score = min(business_score, 100)

    # --------------------------------------------------
    # TECH STACK (Tracking & Conversion Readiness)
    # --------------------------------------------------
    tech_score = 0
    if tech.get("gtm"):
        tech_score += 25
    if tech.get("ga4"):
        tech_score += 25
    if tech.get("fb_pixel"):
        tech_score += 20
    if tech.get("google_ads_pixel"):
        tech_score += 15
    if tech.get("chat_widget"):
        tech_score += 15

    tech_score = min(tech_score, 100)

    # --------------------------------------------------
    # WEBSITE PERFORMANCE (PageSpeed)
    # --------------------------------------------------
    mobile = pagespeed.get("psi_mobile_score")
    desktop = pagespeed.get("psi_desktop_score")

    if mobile is None and desktop is None:
        performance_score = 50   # neutral fallback
    else:
        scores = [s for s in [mobile, desktop] if s is not None]
        performance_score = round(sum(scores) / len(scores), 2)

    # --------------------------------------------------
    # ONLINE REPUTATION (Google + Facebook)
    # --------------------------------------------------
    review_score = 0

    google_total = google.get("google_reviews_total")
    google_rating = google.get("gbp_rating")

    if google_total:
        review_score += 40
    if google_rating and google_rating >= 4:
        review_score += 30

    fb_total = facebook.get("facebook_reviews_total")
    if fb_total:
        review_score += 30

    # fallback for non-local / B2B sites
    if review_score == 0:
        review_score = 50

    review_score = min(review_score, 100)

    # --------------------------------------------------
    # SEO VISIBILITY (REAL DATA)
    # --------------------------------------------------
    visibility_score = seo.get("visibility_score")

    if visibility_score is None:
        seo_score = 50
    else:
        seo_score = round(visibility_score, 2)

    # --------------------------------------------------
    # LISTINGS (GBP presence)
    # --------------------------------------------------
    listings_score = 0
    if google.get("gbp_claimed"):
        listings_score = 100
    elif google_total:
        listings_score = 70
    else:
        listings_score = 40

    # --------------------------------------------------
    # FINAL SECTION MAP
    # --------------------------------------------------
    return {
        "Business Details": business_score,
        "Tech Stack": tech_score,
        "Website Performance": performance_score,
        "Online Reputation": review_score,
        "SEO Analysis": seo_score,
        "Listings": listings_score,
    }
