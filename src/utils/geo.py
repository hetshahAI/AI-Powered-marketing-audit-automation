from urllib.parse import urlparse

def detect_country_code(website_url: str, business_info: dict):
    address = str(business_info.get("address", "")).lower()

    # 1️⃣ Address-based detection (best)
    if "india" in address:
        return "in"
    if "united states" in address or "usa" in address:
        return "us"
    if "uk" in address or "united kingdom" in address:
        return "gb"
    if "australia" in address:
        return "au"

    # 2️⃣ Domain-based fallback
    domain = urlparse(website_url).netloc.lower()

    if domain.endswith(".in"):
        return "in"
    if domain.endswith(".uk"):
        return "gb"
    if domain.endswith(".au"):
        return "au"

    # 3️⃣ GLOBAL SEO (important)
    return None
