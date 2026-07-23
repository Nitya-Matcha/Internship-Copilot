import os
import json
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_job_skills(title):

    prompt = f"""
You are analyzing a software engineering internship.

Extract the important technical skills.

Job title:
{title}

Return ONLY a JSON array.

Example:
[
"Python",
"React",
"SQL",
"AWS"
]
"""


    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0
    )


    text = response.choices[0].message.content


    try:
        skills = json.loads(text)

    except:
        print("Failed parsing:", text)
        skills = [
            "Software Engineering"
        ]


    return skills