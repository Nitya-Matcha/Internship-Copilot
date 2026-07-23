import os
import json
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ai_match_resume(resume_text, jobs):

    jobs_text = ""

    for job in jobs:
        jobs_text += (
            f"Company: {job['company']}\n"
            f"Title: {job['title']}\n"
            f"Location: {job['location']}\n"
            f"URL: {job['url']}\n\n"
        )


    prompt = f"""
You are an AI internship matching assistant.

Analyze the student's resume and compare it against available internships.

Resume:

{resume_text}


Internships:

{jobs_text}


Return ONLY valid JSON.

Return the top internship matches in this exact format:

{{
  "matches": [
    {{
      "company": "Company Name",
      "title": "Internship Title",
      "url": "Internship URL",
      "match_score": 0-100,
      "reason": "Why this internship matches the resume",
      "missing_skills": [
        "skill 1",
        "skill 2"
      ]
    }}
  ]
}}

Do not include markdown.
Do not include explanations outside the JSON.
"""


    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )


    result = response.choices[0].message.content


    matches = json.loads(result)


    # Attach database IDs
    for match in matches["matches"]:

        for job in jobs:

            if (
                match["company"] == job["company"]
                and match["title"] == job["title"]
            ):
                match["id"] = job["id"]
                match["location"] = job["location"]
                break


    return matches