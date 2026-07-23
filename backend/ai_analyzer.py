from openai import OpenAI
import json

client = OpenAI()


def analyze_resume(resume_text):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=[
            {
                "role":"system",
                "content":
                """
Extract technical skills from this resume.

Return ONLY JSON:

{
 "skills": [
   "Python",
   "React",
   "SQL"
 ]
}
"""
            },
            {
                "role":"user",
                "content":resume_text
            }
        ]
    )


    return json.loads(
        response.choices[0].message.content
    )