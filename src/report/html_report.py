from datetime import datetime
import os

def generate_html_report(result: dict, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)

    business_name = result.get("business_info", {}).get(
        "business_name", "Business"
    )



    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"Marketing Audit - {business_name} - {date_str}.html"
    filepath = os.path.join(output_dir, filename)

    rows = ""
    for category, score in result["report_scores"].items():
        rows += f"""
        <tr>
            <td>{category}</td>
            <td>{score}%</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>Marketing Audit - {business_name}</title>
        <style>
            body {{
                font-family: Arial;
                background: #0f172a;
                color: white;
                padding: 40px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #334155;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background: #1e293b;
            }}
            .score {{
                font-size: 40px;
                color: #38bdf8;
            }}
            .section {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>

        <h1>Marketing Audit – {business_name}</h1>
        <p>Date: {date_str}</p>

        <div class="score">
            Overall Score: {result["final_score"]} / 100
        </div>

        <div class="section">
            <h2>Category Scores</h2>
            <table>
                <tr>
                    <th>Category</th>
                    <th>Score</th>
                </tr>
                {rows}
            </table>
        </div>

        <div class="section">
            <h2>AI Observations</h2>
            <pre>{result["ai_audit_report"]}</pre>
        </div>
        
        <div class="section">
            <h2>Raw Audit Data (Collector Outputs)</h2>
            <pre>{result["audit_results"]}</pre>
        </div>


    </body>
    </html>
    """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath
