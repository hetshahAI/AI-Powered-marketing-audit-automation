# collectors/gbp_reviews.py
import os
from urllib.parse import urlparse
from difflib import SequenceMatcher
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

def _safe_float(x):
    try:
        return float(x)
    except Exception:
        return None

def _safe_int(x):
    try:
        return int(x)
    except Exception:
        return None

def _norm_domain(url: str) -> str:
    if not url:
        return ""
    return urlparse(url).netloc.replace("www.", "").lower()

def _name_sim(a: str, b: str) -> float:
    a = (a or "").lower().strip()
    b = (b or "").lower().strip()
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def analyze_google_reviews(reviews: list) -> dict:
    if not reviews:
        return {
            "google_reviews_total": None,
            "google_reviews_positive": None,
            "google_reviews_negative": None,
            "google_reply_rate": None,
            "google_avg_response_time": None,
        }

    total = len(reviews)
    pos = 0
    neg = 0
    replied = 0

    for r in reviews:
        rating = r.get("rating") or r.get("stars") or r.get("reviewRating")
        rating = _safe_float(rating)
        if rating is not None:
            if rating >= 4: pos += 1
            if rating <= 2: neg += 1

        owner_resp = r.get("ownerResponse") or r.get("response") or r.get("reviewReply")
        if owner_resp:
            replied += 1

    reply_rate = round((replied / total) * 100, 2) if total else None

    return {
        "google_reviews_total": total,
        "google_reviews_positive": pos,
        "google_reviews_negative": neg,
        "google_reply_rate": reply_rate,
        "google_avg_response_time": None,
    }

def fetch_gbp_and_google_reviews(search_term: str, location: str = "", target_website: str | None = None) -> dict:
    if not APIFY_API_TOKEN:
        raise RuntimeError("APIFY_API_TOKEN missing in .env")

    client = ApifyClient(APIFY_API_TOKEN)

    ACTOR_ID = "compass/crawler-google-places"

    query = f"{search_term} {location}".strip()

    run_input = {
        "searchStringsArray": [query],
        "maxCrawledPlacesPerSearch": 5,   # 👈 IMPORTANT
        "maxReviews": 200,
        "language": "en",
    }

    run = client.actor(ACTOR_ID).call(run_input=run_input)
    dataset_id = run["defaultDatasetId"]
    items = list(client.dataset(dataset_id).iterate_items())

    if not items:
        return {
            "gbp_claimed": None,
            "gbp_rating": None,
            "gbp_review_count": None,
            "gbp_hours": None,
            "gbp_photos": None,
            "gbp_phone": None,
            "gbp_address": None,
            **analyze_google_reviews([]),
        }

    target_domain = _norm_domain(target_website or "")

    # ✅ choose best place
    best = None
    best_score = -1

    for place in items:
        place_name = place.get("title") or place.get("name") or ""
        place_website = place.get("website") or place.get("url") or ""
        place_domain = _norm_domain(place_website)

        score = 0

        # strongest signal: website domain match
        if target_domain and target_domain and (target_domain in place_domain or place_domain in target_domain):
            score += 100

        # fallback: name similarity
        score += int(_name_sim(search_term, place_name) * 50)

        if score > best_score:
            best_score = score
            best = place

    place = best or items[0]

    gbp_rating = place.get("rating") or place.get("totalScore") or place.get("stars")
    gbp_review_count = place.get("reviewsCount") or place.get("numberOfReviews") or place.get("reviews")
    gbp_phone = place.get("phone") or place.get("phoneNumber") or place.get("internationalPhoneNumber")
    gbp_address = place.get("address") or place.get("fullAddress") or place.get("streetAddress")
    gbp_hours = place.get("openingHours") or place.get("hours")
    gbp_photos = place.get("photosCount") or place.get("totalPhotos")
    gbp_claimed = place.get("claimed") or place.get("isClaimed") or None

    reviews = place.get("reviews") or place.get("reviewsData") or place.get("latestReviews") or []
    review_stats = analyze_google_reviews(reviews if isinstance(reviews, list) else [])

    return {
        "gbp_claimed": gbp_claimed,
        "gbp_rating": _safe_float(gbp_rating),
        "gbp_review_count": _safe_int(gbp_review_count),
        "gbp_hours": gbp_hours if isinstance(gbp_hours, str) else None,
        "gbp_photos": _safe_int(gbp_photos),
        "gbp_phone": gbp_phone,
        "gbp_address": gbp_address,
        **review_stats,
    }
