def detect_business_type(business_info: dict) -> str:
    name = business_info.get("business_name", "").lower()

    if "property" in name:
        return "property"
    if "agency" in name or "marketing" in name:
        return "agency"
    if "software" in name or "saas" in name:
        return "saas"

    return "generic"


def get_dynamic_keywords(business_type: str, business_info: dict):
    base = business_info.get("business_name", "")

    mapping = {
        "property": [
            base,
            "property management",
            "real estate services",
            "homes for rent"
        ],
        "agency": [
            base,
            "digital marketing agency",
            "seo agency",
            "web development agency"
        ],
        "saas": [
            base,
            "software company",
            "saas platform",
            "cloud software"
        ],
        "generic": [
            base,
            "business services",
            "professional services"
        ]
    }

    return mapping.get(business_type, mapping["generic"])
