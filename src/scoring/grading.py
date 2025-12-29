def get_marketing_grade(final_score: float) -> dict:
    """
    Converts final marketing score into grade, risk level, and verdict.
    """

    if final_score >= 90:
        return {
            "grade": "A+",
            "risk_level": "Very Low",
            "verdict": "Excellent digital marketing presence. Strong visibility, trust, and performance."
        }

    elif final_score >= 80:
        return {
            "grade": "A",
            "risk_level": "Low",
            "verdict": "Strong marketing foundations with minor optimization opportunities."
        }

    elif final_score >= 70:
        return {
            "grade": "B",
            "risk_level": "Low–Medium",
            "verdict": "Good overall presence, but some areas are limiting maximum growth."
        }

    elif final_score >= 60:
        return {
            "grade": "C",
            "risk_level": "Medium",
            "verdict": "Average marketing performance. Visibility and conversion improvements needed."
        }

    elif final_score >= 50:
        return {
            "grade": "D",
            "risk_level": "High",
            "verdict": "Weak marketing foundation. Immediate improvements recommended."
        }

    else:
        return {
            "grade": "F",
            "risk_level": "Very High",
            "verdict": "Critical marketing gaps detected. Business is losing visibility and leads."
        }
