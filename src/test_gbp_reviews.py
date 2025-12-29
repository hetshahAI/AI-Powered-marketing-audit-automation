from collectors.gbp_reviews import fetch_gbp_and_google_reviews

# Use business name + city for better match
data = fetch_gbp_and_google_reviews(
    search_term="American Horizon Property Management",
    location="Roseville, CA"
)

for k, v in data.items():
    print(f"{k}: {v}")
