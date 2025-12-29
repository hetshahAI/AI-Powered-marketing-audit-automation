from dotenv import load_dotenv
load_dotenv()

# ============================================================
# COLLECTORS
# ============================================================

from collectors.business_info import extract_business_info
from collectors.tech_stack import detect_tech_stack
from collectors.pagespeed import get_website_performance
from collectors.gbp_reviews import fetch_gbp_and_google_reviews
from collectors.social_links import extract_facebook_url
from collectors.facebook_reviews import fetch_facebook_reviews
from collectors.seo_visibility import get_seo_visibility

from report.html_report import generate_html_report
from storage.excel_store import store_audit_in_excel
from utils.geo import detect_country_code
from utils.keywords import detect_business_type, get_dynamic_keywords

# ============================================================
# SCORING
# ============================================================

from scoring.score_mapper import map_audit_to_scores
from scoring.scoring_engine import calculate_marketing_score
from scoring.grading import get_marketing_grade
from scoring.report_scores import build_report_scores

# ============================================================
# AI
# ============================================================

from ai.langchain_audit_chain import generate_ai_audit


# ============================================================
# 🔑 BUSINESS CONTEXT (CRITICAL FIX)
# ============================================================

def detect_business_type(business_info: dict) -> str:
    name = (business_info.get("business_name") or "").lower()

    if any(k in name for k in ["property", "real estate", "rent"]):
        return "local_service"

    if any(k in name for k in ["agency", "digital", "marketing", "seo", "white label"]):
        return "agency"

    return "generic"


def get_dynamic_keywords(business_type: str, business_info: dict) -> list:
    if business_type == "local_service":
        return [
            "property management",
            "homes for rent",
            "real estate services",
            "rental property management"
        ]

    if business_type == "agency":
        return [
            "white label digital agency",
            "seo outsourcing",
            "wordpress development agency",
            "hire remote developers",
            "marketing agency services"
        ]

    return [business_info.get("business_name", "")]


# ============================================================
# CORE FUNCTION (UI SAFE)
# ============================================================

def run_marketing_audit(website_url: str) -> dict:
    try:
        # -----------------------------
        # STEP 1: BUSINESS INFO
        # -----------------------------
        business_info = extract_business_info(website_url)

        # -----------------------------
        # STEP 2: TECH STACK
        # -----------------------------
        tech_stack = detect_tech_stack(website_url)

        # -----------------------------
        # STEP 3: PERFORMANCE
        # -----------------------------
        pagespeed = get_website_performance(website_url)

        # -----------------------------
        # STEP 4: GOOGLE REVIEWS
        # -----------------------------
        google_reviews = fetch_gbp_and_google_reviews(
            search_term=business_info.get("business_name", ""),
            location=business_info.get("location", "")
        )

        # -----------------------------
        # STEP 5: FACEBOOK REVIEWS
        # -----------------------------
        facebook_url = extract_facebook_url(website_url)
        facebook_reviews = fetch_facebook_reviews(facebook_url) if facebook_url else {}

        # -----------------------------
        # 🔑 STEP 6: SEO (DYNAMIC FIX)
        # -----------------------------
        business_type = detect_business_type(business_info)
        keywords = get_dynamic_keywords(business_type, business_info)

        seo_visibility = get_seo_visibility(
            website_url=website_url,
            keywords=keywords,
            geo_hint=business_info.get("location", ""),
            country_code="us"
        )

        # -----------------------------
        # RAW AUDIT DATA
        # -----------------------------
        audit_results = {
            "business_info": business_info,
            "tech_stack": tech_stack,
            "pagespeed": pagespeed,
            "google_reviews": google_reviews,
            "facebook_reviews": facebook_reviews,
            "seo_visibility": seo_visibility,
        }

        # -----------------------------
        # STEP 7: SCORING ENGINE
        # -----------------------------
        section_scores = map_audit_to_scores(audit_results)

        score_result = calculate_marketing_score(section_scores)
        final_score = score_result["final_score"]
        breakdown = score_result["breakdown"]

        grade = get_marketing_grade(final_score)

        # -----------------------------
        # STEP 8: REPORT SCORES
        # -----------------------------
        report_scores = build_report_scores(
            audit_results=audit_results,
            section_scores=section_scores,
            final_score=final_score
        )

        # -----------------------------
        # STEP 9: AI SUMMARY
        # -----------------------------
        ai_report = generate_ai_audit(
            audit_results,
            final_score,
            grade
        )

        # -----------------------------
        # STEP 10: HTML REPORT
        # -----------------------------
        html_report_path = generate_html_report({
            "business_info": business_info,
            "final_score": final_score,
            "grade": grade,
            "report_scores": report_scores,
            "ai_audit_report": ai_report,
            "audit_results": audit_results
        })

        # -----------------------------
        # STEP 11: EXCEL STORAGE
        # -----------------------------
        excel_path = store_audit_in_excel({
            "website": website_url,
            "business_type": business_type,
            "final_score": final_score,
            "grade": grade,
            "report_scores": report_scores
        })

        # -----------------------------
        # UI RESPONSE
        # -----------------------------
        return {
            "status": "success",
            "website": website_url,
            "business_type": business_type,

            "collectors": audit_results,

            "final_score": final_score,
            "grade": grade,
            "engine_breakdown": breakdown,
            "report_scores": report_scores,

            "ai_summary": ai_report,

            "html_report_path": html_report_path,
            "excel_path": excel_path
        }

    except Exception as e:
        return {
            "status": "error",
            "website": website_url,
            "error": str(e)
        }
