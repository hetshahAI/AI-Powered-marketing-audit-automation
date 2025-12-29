import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from apify_client import ApifyClient

# --------------------------------------------------
# ENV
# --------------------------------------------------
load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise RuntimeError("APIFY_API_TOKEN missing")

client = ApifyClient(APIFY_API_TOKEN)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def normalize_domain(url: str) -> str:
    return urlparse(url).netloc.replace("www.", "").lower()


def rank_to_visibility(rank: int) -> float:
    if rank <= 0:
        return 0.0
    if rank <= 3:
        return 100.0
    if rank <= 10:
        return round(100 - (rank - 3) * 8, 2)
    if rank <= 20:
        return round(40 - (rank - 10) * 2.5, 2)
    if rank <= 50:
        return round(15 - (rank - 20) * 0.45, 2)
    return 0.0


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------
def get_seo_visibility(
    website_url: str,
    keywords: list[str],
    geo_hint: str = "",
    country_code: str = "us",
):
    target_domain = normalize_domain(website_url)

    # ✅ Apify expects newline-separated string
    query_string = "\n".join(
        [f"{kw} {geo_hint}".strip() for kw in keywords]
    )

    run = client.actor("apify/google-search-scraper").call(
        run_input={
            "queries": query_string,
            "resultsPerPage": 20,
            "maxPagesPerQuery": 4,   # ≈ Top 50–60
            "countryCode": country_code,
            "languageCode": "en",
            "mobileResults": False,
        }
    )

    items = client.dataset(run["defaultDatasetId"]).list_items().items

    keyword_rankings = {}
    keyword_visibility = {}

    for item in items:
        search_query = item.get("searchQuery", {})
        query_text = search_query.get("q")

        if not query_text:
            continue

        organic_results = item.get("organicResults", [])
        rank = 0

        for idx, result in enumerate(organic_results, start=1):
            result_url = result.get("url", "")
            if not result_url:
                continue

            result_domain = normalize_domain(result_url)

            if target_domain in result_domain:
                rank = idx
                break

        keyword_rankings[query_text] = rank
        keyword_visibility[query_text] = rank_to_visibility(rank)

    visibility_score = (
        round(sum(keyword_visibility.values()) / len(keyword_visibility), 2)
        if keyword_visibility else 0.0
    )

    return {
        "keyword_rankings": keyword_rankings,
        "keyword_visibility": keyword_visibility,
        "visibility_score": visibility_score,
    }
