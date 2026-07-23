from openai import OpenAI

client = OpenAI()

def analyze_resume(resume_text):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert software engineering internship recruiter.
                """
            },
            {
                "role": "user",
                "content": f"""
                Analyze this resume:

                {resume_text}

                Return:
                - Key skills
                - Strengths
                - Weaknesses
                - Missing skills
                - Recommended projects
                """
            }
        ]
    )

    return response.choices[0].message.content