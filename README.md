
#🚀 Marketing Audit Automation Platform (AI-Powered)

**A production-grade AI system that audits any website’s digital marketing presence and generates actionable business intelligence.**

This project performs a **full marketing audit** for any website — covering **SEO visibility, online reputation, tech stack, website performance, scoring engine, and AI-generated insights** — and outputs **downloadable reports** (HTML + Excel).

Built to handle **real-world websites**, not demos.

---

## 🧠 Why This Project Exists

Most businesses have **no single system** to answer:
- Why am I not ranking on Google?
- How strong is my online reputation?
- Is my website technically optimized?
- Where am I losing leads?
- What should I fix first?

👉 This platform answers **all of that automatically**, using **AI + data scraping + scoring logic**.

---

## ✨ Key Capabilities

### 🔍 Universal Website Audit
Works for:
- SaaS products
- Digital agencies
- Local businesses
- Enterprise websites

Handles:
- Geo differences
- Blocked pages
- Missing data
- Captchas & partial failures (fails safely)

---

### 📊 What It Analyzes

| Area                      | What We Measure                                                          |
|----                       |----                                                 |
| **Business Intelligence** | Name, contact signals, platform hints               |
| **SEO Visibility**        | Google rankings, keyword positions, visibility score|
| **Google Reviews (GBP)**  | Rating, review count, reply rate                    |
| **Facebook Reviews**      | Sentiment analysis, reply behavior                  |
| **Tech Stack**            | GA4, GTM, Meta Pixel, Ads Pixel, Chat widgets       |
| **Website Performance**   | PageSpeed, Core Web Vitals                          |
| **Scoring Engine**        | Weighted 0–100 marketing score                      |
| **AI Analysis**           | Strengths, weaknesses, recommendations              |

---

## 🧠 AI-Powered Insights (Not Static Text)

The AI layer:
- Reads **real scraped data**
- Understands **business context**
- Generates:
  - Executive summary
  - Top strengths
  - Critical weaknesses
  - Actionable recommendations

No templates. No fake insights.

---

## 🏗️ System Architecture

```

User / UI
↓
main.py (Audit Orchestrator)
↓
Collectors Layer (Apify + HTTP)
↓
Scoring Engine (Weighted Logic)
↓
AI Reasoning (LangChain)
↓
Reports (HTML + Excel)

```

---

## 🗂 Project Structure

```

marketing-audit-automation/
│
├── src/
│   ├── collectors/        # SEO, reviews, tech stack, performance
│   ├── scoring/           # Scoring engine, weights, grading
│   ├── ai/                # AI audit summary (LangChain)
│   ├── report/            # HTML report generator
│   ├── storage/           # Excel export
│   ├── utils/             # Geo & keyword helpers
│   ├── ui/                # Streamlit frontend
│   └── main.py            # Core audit runner
│
├── reports/               # Generated HTML reports
├── audit_data.xlsx        # Excel audit storage
├── .env.example           # Safe environment template
├── .gitignore
├── requirements.txt
└── README.md

````

---

## 🔧 Technologies & Why They Were Used

| Tool                         | Why It Was Chosen |
|----        |----     |
| **Python** | Core orchestration & data processing |
| **Apify** | Reliable SERP, reviews & social scraping |
| **Streamlit** | Fast, clean frontend for audits |
| **LangChain** | Structured AI reasoning (not prompt hacks) |
| **Google PageSpeed API** | Real Core Web Vitals |
| **BeautifulSoup** | HTML parsing for social links |
| **Requests** | Lightweight HTTP calls |
| **Excel (openpyxl/pandas)** | Business-friendly data export |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/marketing-audit-automation.git
cd marketing-audit-automation
````

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

```bash
cp .env
```

Add your API keys inside `.env`.

---

## ▶️ Run Backend (CLI Mode)

```bash
python src/main.py
```

---

## 🖥 Run Frontend (Streamlit UI)

```bash
streamlit run src/ui/app.py
```

---

## 📄 Outputs

| Output            | Location          |
| ----------------- | ----------------- |
| HTML Audit Report | `/reports/`       |
| Excel Audit Data  | `audit_data.xlsx` |
| AI Summary        | UI + HTML         |

---

## 🧪 Tested On

* SaaS platforms (Odoo , E2M solutions , americanpropertymanagement)
* Digital agencies
* Local service businesses
* High-content enterprise websites

---

## 🚧 Future Enhancements

* Competitor comparison
* SERP screenshots
* Automated email reports
* CRM integration
* Lead scoring

---

## 👤 Author

**Het Shah**
AI & Automation Engineer

🔗 **GitHub**: [hetshah's github](https://github.com/hetshahAI)
🔗 **LinkedIn**: [hetshah's linkedin](https://www.linkedin.com/in/hetshah-AI-tech/)


