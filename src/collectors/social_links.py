# collectors/social_links.py
import re
import requests
from bs4 import BeautifulSoup

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

HEADERS = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}

def _clean_fb(url: str) -> str | None:
    if not url:
        return None
    u = url.strip()

    # ignore share dialogs or intent links
    bad = ["sharer.php", "/share", "intent", "dialog/share"]
    if any(b in u for b in bad):
        return None

    # normalize protocol
    if u.startswith("//"):
        u = "https:" + u
    if u.startswith("http://") or u.startswith("https://"):
        return u
    return None

def extract_facebook_url(website_url: str) -> str | None:
    try:
        r = requests.get(website_url, headers=HEADERS, timeout=20, allow_redirects=True)
        r.raise_for_status()
        html = r.text
    except Exception:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # 1) direct anchors
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "facebook.com" in href or "fb.me" in href:
            cleaned = _clean_fb(href)
            if cleaned:
                return cleaned

    # 2) JSON-LD sameAs
    for script in soup.find_all("script", {"type": "application/ld+json"}):
        txt = script.get_text(" ", strip=True)
        if "facebook.com" in txt or "fb.me" in txt:
            m = re.search(r"https?://(www\.)?(facebook\.com|fb\.me)/[^\s\"']+", txt)
            if m:
                cleaned = _clean_fb(m.group(0))
                if cleaned:
                    return cleaned

    # 3) raw regex search in full HTML (sometimes embedded)
    m = re.search(r"https?://(www\.)?(facebook\.com|fb\.me)/[^\s\"']+", html)
    if m:
        cleaned = _clean_fb(m.group(0))
        if cleaned:
            return cleaned

    return None
