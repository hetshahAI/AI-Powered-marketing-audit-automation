from pydantic import BaseModel
from typing import List, Optional, Dict


class AuditMetrics(BaseModel):
    #BASIC INFO
    url: str
    business_name: Optional[str] = None
    scrape_date: str  # ISO format datetime string

    #BUSINESS INFORMATION
    phones: List[str]
    address: Optional[str] = None
    hours: Optional[str] = None
    text_enabled: bool
    contact_page: bool
    platform_hint: Optional[str] = None

    #TECHNOLOGY STACK
    gtm: bool
    ga_ua: bool
    ga4: bool
    fb_pixel: bool
    google_ads_pixel: bool
    chat_widget: bool

    #GOOGLE BUSINESS PROFILE
    gbp_claimed: Optional[bool] = None
    gbp_rating: Optional[float] = None
    gbp_review_count: Optional[int] = None
    gbp_hours: Optional[str] = None
    gbp_photos: Optional[int] = None
    gbp_phone: Optional[str] = None
    gbp_address: Optional[str] = None

    #GOOGLE REVIEWS
    google_reviews_total: Optional[int] = None
    google_reviews_positive: Optional[int] = None
    google_reviews_negative: Optional[int] = None
    google_reply_rate: Optional[float] = None
    google_avg_response_time: Optional[float] = None

    #FACEBOOK REVIEWS
    facebook_reviews_total: Optional[int] = None
    facebook_reviews_positive: Optional[int] = None
    facebook_reviews_negative: Optional[int] = None
    facebook_reply_rate: Optional[float] = None
    facebook_avg_response_time: Optional[float] = None
    facebook_reviews_unknown: Optional[int] = None


    #WEBSITE PERFORMANCE
    psi_mobile_score: Optional[float] = None
    psi_desktop_score: Optional[float] = None
    fcp: Optional[float] = None
    lcp: Optional[float] = None
    tbt: Optional[float] = None
    cls: Optional[float] = None

    #SEO VISIBILITY
    keyword_rankings: Dict[str, int]
    visibility_score: float

    #SCORING 
    business_score: float
    tech_score: float
    gbp_score: float
    listings_score: float
    reputation_score: float
    website_score: float
    seo_score: float
    overall_score: float
    grade: str
