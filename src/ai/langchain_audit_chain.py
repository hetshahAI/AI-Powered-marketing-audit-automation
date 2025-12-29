from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os


def generate_ai_audit(audit_results, final_score, grade):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    prompt = PromptTemplate(
        input_variables=["audit", "score", "grade"],
        template="""
You are a senior digital marketing auditor.

Website audit data:
{audit}

Final Score: {score}/100
Grade: {grade}

Give:
1. Executive summary (2–3 lines)
2. Top 3 strengths
3. Top 3 weaknesses
4. Actionable recommendations
"""
    )

    chain = prompt | llm

    response = chain.invoke({
        "audit": audit_results,
        "score": final_score,
        "grade": grade
    })

    return response.content
