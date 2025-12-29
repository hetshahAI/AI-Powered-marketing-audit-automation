import streamlit as st
import pandas as pd
import os
import sys

# --------------------------------------------------
# Fix import path (CRITICAL – no more src errors)
# --------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from main import run_marketing_audit


# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Marketing Audit Automation",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🚀 Marketing Audit Automation")
st.markdown(
    """
Generate a **full AI-powered marketing audit** for any website  
including **SEO, Reviews, Tech Stack, Scoring Engine & AI Insights**
"""
)

st.divider()

# --------------------------------------------------
# URL Input
# --------------------------------------------------
website_url = st.text_input(
    "🌐 Enter Website URL",
    placeholder="https://www.example.com"
)

run_btn = st.button("🔍 Run Marketing Audit")

# --------------------------------------------------
# Run Audit
# --------------------------------------------------
if run_btn and website_url:
    with st.spinner("Running audit... this may take 1–2 minutes"):
        result = run_marketing_audit(website_url)

    if result["status"] != "success":
        st.error(f"❌ Audit failed: {result.get('error')}")
        st.stop()

    st.success("✅ Audit completed successfully!")

    # ==================================================
    # FINAL SCORE
    # ==================================================
    st.subheader("🎯 Final Score")
    col1, col2 = st.columns([1, 3])

    with col1:
        st.metric("Score", f"{result['final_score']} / 100")

    with col2:
        st.json(result["grade"])

    st.divider()

    # ==================================================
    # CATEGORY SCORES
    # ==================================================
    st.subheader("📊 Category Scores")

    score_df = pd.DataFrame(
        result["report_scores"].items(),
        columns=["Category", "Score (%)"]
    )

    st.dataframe(score_df, use_container_width=True)
    st.bar_chart(score_df.set_index("Category"))

    st.divider()

    # ==================================================
    # AI SUMMARY
    # ==================================================
    st.subheader("🧠 AI Marketing Summary")
    st.markdown(result["ai_summary"])

    st.divider()

    # ==================================================
    # RAW COLLECTOR OUTPUTS (PROOF FOR SIR)
    # ==================================================
    st.subheader("🔍 Collector Outputs (Technical Proof)")

    collectors = result["collectors"]

    for section, data in collectors.items():
        with st.expander(section.replace("_", " ").title(), expanded=False):
            if isinstance(data, dict):
                df = pd.DataFrame(
                    data.items(),
                    columns=["Metric", "Value"]
                )
                st.dataframe(df, use_container_width=True)
            else:
                st.write(data)

    st.divider()

    # ==================================================
    # DOWNLOAD FILES
    # ==================================================
    st.subheader("📄 Download Audit Files")

    col1, col2 = st.columns(2)

    # HTML REPORT
    if result.get("html_report_path") and os.path.exists(result["html_report_path"]):
        with open(result["html_report_path"], "r", encoding="utf-8") as f:
            col1.download_button(
                label="📄 Download HTML Report",
                data=f.read(),
                file_name=os.path.basename(result["html_report_path"]),
                mime="text/html"
            )

    # EXCEL FILE
    if result.get("excel_path") and os.path.exists(result["excel_path"]):
        with open(result["excel_path"], "rb") as f:
            col2.download_button(
                label="📊 Download Excel Sheet",
                data=f,
                file_name=os.path.basename(result["excel_path"]),
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.divider()

    st.success("🎉 Marketing Audit Completed Successfully!")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
---
Built with ❤️ using **Python · Streamlit · LangChain · Apify**  
_AI-Powered Marketing Audit Automation_
"""
)
