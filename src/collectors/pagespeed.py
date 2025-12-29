import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY")


def get_website_performance(url: str) -> dict:
    """
    Fetches PageSpeed Insights and Core Web Vitals.
    """

    result = {
        "psi_mobile_score": None,
        "psi_desktop_score": None,
        "fcp": None,
        "lcp": None,
        "tbt": None,
        "cls": None,
    }

    if not PAGESPEED_API_KEY:
        print("PageSpeed API key missing")
        return result

    for strategy in ["mobile", "desktop"]:
        api_url = (
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            f"?url={url}&strategy={strategy}&category=performance&key={PAGESPEED_API_KEY}"
        )

        try:
            response = requests.get(api_url, timeout=20)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"PageSpeed API error ({strategy}):", e)
            continue

        lighthouse = data.get("lighthouseResult", {})
        categories = lighthouse.get("categories", {})
        audits = lighthouse.get("audits", {})

        score = categories.get("performance", {}).get("score")
        if score is not None:
            score = round(score * 100, 2)

        if strategy == "mobile":
            result["psi_mobile_score"] = score
        else:
            result["psi_desktop_score"] = score

        # Core Web Vitals (convert ms → seconds where needed)
        def audit_value(key):
            val = audits.get(key, {}).get("numericValue")
            if val is not None:
                return round(val / 1000, 2)
            return None

        result["fcp"] = audit_value("first-contentful-paint")
        result["lcp"] = audit_value("largest-contentful-paint")
        result["tbt"] = audit_value("total-blocking-time")
        result["cls"] = audits.get("cumulative-layout-shift", {}).get("numericValue")

    return result
