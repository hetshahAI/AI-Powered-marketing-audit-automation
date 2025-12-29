from collectors.social_links import extract_facebook_url
from collectors.facebook_reviews import fetch_facebook_reviews

website_url = "https://www.odoo.com/"

facebook_url = extract_facebook_url(website_url)
print("Facebook URL:", facebook_url)

fb_reviews = fetch_facebook_reviews(facebook_url)

for k, v in fb_reviews.items():
    print(f"{k}: {v}")
