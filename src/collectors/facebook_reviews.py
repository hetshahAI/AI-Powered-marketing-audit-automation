import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")


def analyze_facebook_reviews(reviews: list) -> dict:
    """
    Analyzes Facebook reviews / recommendations robustly.
    Handles different actor field formats.
    """
    if not reviews:
        return {
            "facebook_reviews_total": None,
            "facebook_reviews_positive": None,
            "facebook_reviews_negative": None,
            "facebook_reviews_unknown": None,
            "facebook_reply_rate": None,
            "facebook_avg_response_time": None,
        }

    total = len(reviews)
    positive = 0
    negative = 0
    unknown = 0
    replied = 0

    def to_bool_like(x):
        """Convert various yes/no/true/false formats to boolean-like or None."""
        if x is None:
            return None
        if isinstance(x, bool):
            return x
        s = str(x).strip().lower()
        if s in ["true", "yes", "y", "recommended", "positive", "recommend"]:
            return True
        if s in ["false", "no", "n", "not recommended", "not_recommended", "negative", "notrecommend"]:
            return False
        return None

    for r in reviews:
        # Possible fields from different scrapers
        rec_raw = (
            r.get("recommended")
            or r.get("is_recommended")
            or r.get("isRecommended")
            or r.get("recommendation")
            or r.get("recommendationType")
        )

        rec = to_bool_like(rec_raw)

        if rec is True:
            positive += 1
        elif rec is False:
            negative += 1
        else:
            # Try rating/stars fallback if present
            rating = r.get("rating") or r.get("stars")
            if rating is not None:
                try:
                    rating = float(rating)
                    if rating >= 4:
                        positive += 1
                    elif rating <= 2:
                        negative += 1
                    else:
                        unknown += 1
                except Exception:
                    unknown += 1
            else:
                unknown += 1

        # Owner reply detection (varies by output)
        if r.get("response") or r.get("ownerResponse") or r.get("reply"):
            replied += 1

    reply_rate = round((replied / total) * 100, 2) if total else None

    return {
        "facebook_reviews_total": total,
        "facebook_reviews_positive": positive,
        "facebook_reviews_negative": negative,
        "facebook_reviews_unknown": unknown,
        "facebook_reply_rate": reply_rate,
        "facebook_avg_response_time": None,
    }



def fetch_facebook_reviews(facebook_page_url: str | None) -> dict:
    """
    Fetches Facebook reviews using Apify.
    """
    if not facebook_page_url:
        return {
            "facebook_reviews_total": None,
            "facebook_reviews_positive": None,
            "facebook_reviews_negative": None,
            "facebook_reply_rate": None,
            "facebook_avg_response_time": None,
        }

    if not APIFY_API_TOKEN:
        raise RuntimeError("APIFY_API_TOKEN missing")

    client = ApifyClient(APIFY_API_TOKEN)

    # Popular and stable Facebook reviews actor
    ACTOR_ID = "apify/facebook-reviews-scraper"

    run_input = {
        "startUrls": [{"url": facebook_page_url}],
        "maxReviews": 200,
        "language": "en",
    }

    run = client.actor(ACTOR_ID).call(run_input=run_input)
    dataset_id = run["defaultDatasetId"]
    items = list(client.dataset(dataset_id).iterate_items())

    return analyze_facebook_reviews(items)
