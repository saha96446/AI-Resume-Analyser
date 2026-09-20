import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def analyze_resume(resume_text):

    prompt = f"""
You are an expert HR Resume Analyzer.

Analyze this resume carefully:

{resume_text}

Return ONLY valid JSON in this format:

{{
    "candidate_name": "",
    "email": "",
    "phone": "",
    "education": [],
    "experience": [],
    "skills": [],
    "certifications": [],
    "projects": [],
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "resume_score": 0,
    "job_matches": [
        {{
            "title": "",
            "match_score": 0,
            "why_match": "",
            "missing_skills": []
        }}
    ],
    "improved_resume": {{
        "professional_summary": "",
        "skills": [],
        "ats_keywords": [],
        "experience": [
            {{
                "role": "",
                "company": "",
                "duration": "",
                "description": ""
            }}
        ],
        "projects": [
            {{
                "title": "",
                "duration": "",
                "tech_stack": "",
                "description": ""
            }}
        ]
    }}
}}

Resume score must be between 0 and 100.
Suggest 3 realistic job roles based only on the candidate's skills and
experience. Each job match score must be between 0 and 100.
If the resume_score is below 80, create an improved_resume optimized for a
90+ ATS-readiness target. Strengthen clarity, action verbs and relevant
keywords, but NEVER invent employers, dates, metrics, credentials, skills,
projects or responsibilities. Use only information in the source resume.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)
