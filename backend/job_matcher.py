def match_jobs(skills, jobs):

    matches = []


    for job in jobs:

        score = 0


        job_text = (
            (job.title or "") +
            " " +
            (job.skills or "")
        ).lower()


        for skill in skills:

            if skill.lower() in job_text:
                score += 1


        matches.append(
            {
                "company": job.company,
                "title": job.title,
                "location": job.location,
                "url": job.url,
                "score": score
            }
        )


    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return matches[:10]