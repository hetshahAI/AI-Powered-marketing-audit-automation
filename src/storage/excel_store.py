import pandas as pd
import os
from datetime import datetime
import re


def safe_filename(text: str):
    text = re.sub(r"[^\w\s-]", "", text)
    return text.replace(" ", "_").lower()


def store_audit_in_excel(audit_data: dict, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)

    website = audit_data.get("website", "website")
    safe_site = safe_filename(website.replace("https://", "").replace("http://", ""))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"audit_{safe_site}_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)

    # Flatten for Excel
    row = {
        "Website": website,
        "Final Score": audit_data.get("final_score"),
        "Grade": audit_data.get("grade", {}).get("grade"),
    }

    for k, v in audit_data.get("report_scores", {}).items():
        row[k] = v

    df = pd.DataFrame([row])

    # SAFE WRITE
    df.to_excel(filepath, index=False)

    return filepath
