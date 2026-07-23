import json
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_resume_skills(resume_text):

    prompt = f"""
Extract the technical skills from this resume.

Return ONLY a JSON array.

Example:
[
"Python",
"React",
"SQL",
"FastAPI"
]

Resume:
{resume_text}
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


    content = response.choices[0].message.content

    return json.loads(content)