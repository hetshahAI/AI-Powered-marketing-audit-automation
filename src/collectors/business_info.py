import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def clean_address(raw_address: str) -> str:
    """
    Cleans noisy footer address text.
    """
    if not raw_address:
        return None

    # Stop at common noise keywords
    stop_keywords = [
        "by phone", "phone:", "fax", "copyright",
        "quick links", "powered by", "all rights reserved"
    ]

    cleaned = raw_address.lower()

    for keyword in stop_keywords:
        if keyword in cleaned:
            cleaned = cleaned.split(keyword)[0]

    # Remove extra spaces
    cleaned = " ".join(cleaned.split())

    # Capitalize nicely
    return cleaned.title()


def extract_business_info(url: str) -> dict:
    """
    Extracts basic business information from a website.
    """

    result = {
        "business_name": None,
        "phones": [],
        "address": None,
        "hours": None,
        "text_enabled": False,
        "contact_page": False,
        "platform_hint": None,
    }


    # 1. Fetch website HTML
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("Error fetching website:", e)
        return result

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # 2. Business name (title or h1)
    if soup.title and soup.title.text:
        result["business_name"] = soup.title.text.strip()

    h1 = soup.find("h1")
    if h1 and h1.text:
        result["business_name"] = h1.text.strip()

    # 3. Phone numbers (US-style)
    phone_pattern = re.compile(r'(\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4})')
    phones = phone_pattern.findall(html)
    result["phones"] = list(set(phones))

    # 4. Contact page detection
    for link in soup.find_all("a", href=True):
        if "contact" in link["href"].lower():
            result["contact_page"] = True
            break

    # 5. Text-enabled number detection (heuristic)
    text_keywords = ["text us", "sms", "text message", "texting"]
    page_text = soup.get_text(separator=" ").lower()
    for keyword in text_keywords:
        if keyword in page_text:
            result["text_enabled"] = True
            break

    # 6. Address detection (best-effort, safe)
    address_candidates = []

    for tag in soup.find_all(["p", "span", "div"]):
        text = tag.get_text(" ", strip=True)
        if re.search(r'\d{5}', text) and re.search(r'\d{1,5}', text):
            if any(word in text.lower() for word in [
                "drive", "dr", "street", "st", "road", "rd",
                "avenue", "ave", "blvd", "lane", "ln"
            ]):
                address_candidates.append(text)

    if address_candidates:
        # Pick the longest one (usually most complete)
        result["address"] = max(address_candidates, key=len)



    # 7. Hours detection
    hours_keywords = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    if any(day in page_text for day in hours_keywords):
        result["hours"] = "Hours information found on page"

    # 8. Platform hint detection
    platform_hints = ["wordpress", "shopify", "wix", "squarespace", "freerentalsite"]
    for platform in platform_hints:
        if platform in page_text:
            result["platform_hint"] = platform.capitalize()
            break

    # Clean address if found
    if result["address"]:
        result["address"] = clean_address(result["address"])

    return result

