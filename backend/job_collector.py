import requests
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Job

from job_skill_extractor import extract_job_skills
import re


# Greenhouse companies
GREENHOUSE_BOARDS = {
    "OpenAI": "openai",
    "Stripe": "stripe",
    "Datadog": "datadog",
    "Cloudflare": "cloudflare",
}


# Lever companies
LEVER_BOARDS = {
    "Netflix": "netflix",
    "Coinbase": "coinbase",
}


# Keywords to identify SWE/technical internships
SWE_KEYWORDS = [
    "software",
    "developer",
    "engineering",
    "frontend",
    "backend",
    "full stack",
    "full-stack",
    "mobile",
    "ios",
    "android",
    "machine learning",
    "ml",
    "ai",
    "data engineer",
    "platform",
    "infrastructure",
    "cloud",
    "security",
    "devops",
]


def is_software_role(title):

    title = title.lower()

    for keyword in SWE_KEYWORDS:
        if keyword in title:
            return True

    return False



def fetch_greenhouse_jobs(company, board):

    url = (
        f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
    )

    try:
        response = requests.get(
            url,
            timeout=10
        )

    except Exception as e:
        print(f"Failed request for {company}: {e}")
        return []


    if response.status_code != 200:

        print(
            f"Failed to fetch {company}: {response.status_code}"
        )

        return []


    data = response.json()

    jobs = []


    for job in data.get("jobs", []):

        title = job.get(
            "title",
            ""
        )


        # Internship filter
        if not re.search(r"\bintern(ship)?\b", title.lower()):
            continue


        # SWE filter
        if not is_software_role(title):
            continue



        location = (
            job.get("location", {})
            .get(
                "name",
                "Remote"
            )
        )


        job_url = job.get(
            "absolute_url",
            ""
        )


        try:

            # ONLY title goes to AI
            skills = extract_job_skills(
                title
            )


        except Exception as e:

            print(
                f"Skill extraction failed for {title}: {e}"
            )

            skills = [
                "Software Engineering"
            ]


        print("ADDING:", title)
        
        jobs.append({

            "company": company,

            "title": title,

            "location": location,

            "url": job_url,

            "skills": ", ".join(skills)

        })


    return jobs





def fetch_lever_jobs(company, board):

    url = (
        f"https://api.lever.co/v0/postings/{board}"
    )


    try:

        response = requests.get(
            url,
            timeout=10
        )

    except Exception as e:

        print(e)
        return []



    if response.status_code != 200:
        return []


    data = response.json()

    jobs = []



    for job in data:


        title = job.get(
            "text",
            ""
        )


        if not re.search(r"\bintern(ship)?\b", title.lower()):
            continue


        if not is_software_role(title):
            continue



        try:

            skills = extract_job_skills(
                title
            )


        except Exception as e:

            print(
                f"Skill extraction failed for {title}: {e}"
            )

            skills = [
                "Software Engineering"
            ]



        jobs.append({

            "company": company,

            "title": title,

            "location":
                job.get(
                    "categories",
                    {}
                )
                .get(
                    "location",
                    "Remote"
                ),

            "url":
                job.get(
                    "hostedUrl"
                ),

            "skills":
                ", ".join(skills)

        })


    return jobs





def save_jobs(jobs):

    db: Session = SessionLocal()


    added = 0


    for job in jobs:


        existing = (
            db.query(Job)
            .filter(
                Job.url == job["url"]
            )
            .first()
        )


        if existing:
            continue



        new_job = Job(

            company=job["company"],

            title=job["title"],

            location=job["location"],

            url=job["url"],

            skills=job["skills"]

        )


        db.add(new_job)

        added += 1



    db.commit()

    db.close()


    print(
        f"Added {added} new internships"
    )





def collect_jobs():

    all_jobs = []


    print(
        "Collecting Greenhouse jobs..."
    )


    for company, board in GREENHOUSE_BOARDS.items():

        jobs = fetch_greenhouse_jobs(
            company,
            board
        )

        all_jobs.extend(jobs)



    print(
        "Collecting Lever jobs..."
    )


    for company, board in LEVER_BOARDS.items():

        jobs = fetch_lever_jobs(
            company,
            board
        )

        all_jobs.extend(jobs)



    print(
        f"Found {len(all_jobs)} SWE internships"
    )


    save_jobs(all_jobs)


    return all_jobs





if __name__ == "__main__":

    collect_jobs()