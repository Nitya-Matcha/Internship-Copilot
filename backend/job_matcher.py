def match_jobs(skills, jobs):

    matches = []

    for job in jobs:

        score = 0
        matched_skills = []
        missing_skills = []

        job_skills = [
            skill.strip()
            for skill in job.skills.split(",")
            if skill.strip()
        ]


        for skill in skills:

            found = False

            for job_skill in job_skills:

                if skill.lower() in job_skill.lower():
                    found = True
                    break


            if found:
                score += 1
                matched_skills.append(skill)

            else:
                missing_skills.append(skill)



        matches.append({

            "company": job.company,

            "title": job.title,

            "location": job.location,

            "url": job.url,

            "skills": job_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "match_score": score

        })



    matches.sort(
        key=lambda x:x["match_score"],
        reverse=True
    )


    return matches[:10]