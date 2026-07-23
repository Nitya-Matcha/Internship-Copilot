def match_resume_to_jobs(resume_text, jobs):

    resume_text = resume_text.lower()

    scored_jobs = []

    for job in jobs:

        score = 0

        title = job["title"].lower()

        if "python" in resume_text:
            score += 10

        if "java" in resume_text:
            score += 10

        if "aws" in resume_text:
            score += 15

        if "software" in title:
            score += 20

        scored_jobs.append({
            **job,
            "score": score
        })

    return sorted(
        scored_jobs,
        key=lambda x: x["score"],
        reverse=True
    )