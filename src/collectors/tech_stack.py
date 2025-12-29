# collectors/tech_stack.py
import re
import requests
from bs4 import BeautifulSoup

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
}

def detect_tech_stack(url: str) -> dict:
    result = {
        "gtm": False,
        "ga_ua": False,
        "ga4": False,
        "fb_pixel": False,
        "google_ads_pixel": False,
        "chat_widget": False,
    }

    try:
        with requests.Session() as s:
            r = s.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
            r.raise_for_status()
            html_raw = r.text
    except Exception:
        return result

    html = html_raw.lower()
    soup = BeautifulSoup(html_raw, "html.parser")

    # collect script src links too
    script_srcs = " ".join(
        [ (tag.get("src") or "") for tag in soup.find_all("script") ]
    ).lower()

    blob = html + "\n" + script_srcs

    # GTM
    if re.search(r"gtm-[0-9a-z]+", blob) or "googletagmanager.com/gtm.js" in blob:
        result["gtm"] = True

    # GA UA
    if re.search(r"\bua-\d{4,}-\d+\b", blob):
        result["ga_ua"] = True

    # GA4 (G-XXXXXXX)
    if re.search(r"\bg-[0-9a-z]{6,}\b", blob) or "gtag('config'" in blob or "google-analytics.com/g/collect" in blob:
        result["ga4"] = True

    # Facebook Pixel
    if "connect.facebook.net" in blob or "fbq(" in blob or "facebook pixel" in blob:
        result["fb_pixel"] = True

    # Google Ads
    if "googleadservices.com" in blob or re.search(r"\baw-\d+\b", blob):
        result["google_ads_pixel"] = True

    # Chat widgets
    chat_patterns = [
        "tawk.to", "intercom", "drift", "crisp.chat", "zendesk",
        "hubspot", "livechat", "freshchat", "chatwoot"
    ]
    result["chat_widget"] = any(p in blob for p in chat_patterns)

    return result
