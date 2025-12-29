from .weights import WEIGHTS
from .score_utils import weighted_score


def calculate_marketing_score(section_scores: dict) -> dict:
    """
    section_scores example:
    {
        "Business Details": 85,
        "Tech Stack": 70,
        "Website Performance": 65,
        "Online Reputation": 80,
        "SEO Analysis": 55,
        "Listings": 90
    }
    """

    breakdown = {}
    total_score = 0.0

    for section, weight in WEIGHTS.items():
        raw_score = section_scores.get(section)

        # Safety fallback (never hard zero unless intended)
        if raw_score is None:
            raw_score = 50

        contribution = weighted_score(raw_score, weight)

        breakdown[section] = {
            "raw_score": round(raw_score, 2),
            "weight": weight,
            "contribution": round(contribution, 2)
        }

        total_score += contribution

    return {
        "final_score": round(total_score, 2),
        "breakdown": breakdown
    }
