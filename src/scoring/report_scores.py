def build_report_scores(audit_results, section_scores, final_score):
    """
    Converts internal engine scores into human-readable audit table
    """

    return {
        "Overall Score": round(final_score),
        "Business Details": 100 if audit_results.get("business_info") else 0,
        "Techno Stack": section_scores.get("website", 0),
        "Google Business Profile": 100 if audit_results.get("google_reviews") else 0,
        "Listings": 0,  # future: Yelp, Bing, Apple Maps
        "Online Reputation": section_scores.get("reviews", 0),
        "Website Performance": section_scores.get("website", 0),
        "SEO Analysis": section_scores.get("seo", 0),
    }
