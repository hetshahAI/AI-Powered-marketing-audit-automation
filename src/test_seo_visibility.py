from collectors.seo_visibility import get_seo_visibility

url = "https://www.americanhorizonproperty.com/"

keywords = [
    "property management",
    "property management company",
    "homes for rent",
]

geo_hint = "Roseville CA"

data = get_seo_visibility(
    website_url=url,
    keywords=keywords,
    geo_hint=geo_hint,
    country_code="us"
)

print("visibility_score:", data["visibility_score"])
print("keyword_rankings:")
for k, v in data["keyword_rankings"].items():
    print(" -", k, "=>", v)

print("keyword_visibility:")
for k, v in data["keyword_visibility"].items():
    print(" -", k, "=>", v)
