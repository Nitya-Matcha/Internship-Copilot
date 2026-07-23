import requests
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Job


# Companies using Greenhouse
GREENHOUSE_BOARDS = {
    "OpenAI": "openai",
    "Stripe": "stripe",
    "Datadog": "datadog",
    "Cloudflare": "cloudflare",
}


# Companies using Lever
LEVER_BOARDS = {
    "Netflix": "netflix",
    "Coinbase": "coinbase",
}


def fetch_greenhouse_jobs(company, board):

    url = (
        f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    jobs = []


    for job in data.get("jobs", []):

        title = job.get("title","")


        # Only internships
        if "intern" not in title.lower():
            continue


        jobs.append({

            "company": company,

            "title": title,

            "location":
                job.get("location", {})
                .get("name","Remote"),

            "url":
                job.get("absolute_url"),

            "skills":
                "Software Engineering, Programming"

        })


    return jobs



def fetch_lever_jobs(company, board):

    url = (
        f"https://api.lever.co/v0/postings/{board}"
    )


    response = requests.get(url)


    if response.status_code != 200:
        return []


    data = response.json()


    jobs=[]


    for job in data:


        title = job.get("text","")


        if "intern" not in title.lower():
            continue


        jobs.append({

            "company":company,

            "title":title,

            "location":
                job.get("categories",{})
                .get("location","Remote"),

            "url":
                job.get("hostedUrl"),

            "skills":
                "Software Engineering"

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


    all_jobs=[]


    print("Collecting Greenhouse jobs...")


    for company,board in GREENHOUSE_BOARDS.items():

        jobs = fetch_greenhouse_jobs(
            company,
            board
        )

        all_jobs.extend(jobs)



    print("Collecting Lever jobs...")


    for company,board in LEVER_BOARDS.items():

        jobs = fetch_lever_jobs(
            company,
            board
        )

        all_jobs.extend(jobs)



    print(
        f"Found {len(all_jobs)} internships"
    )


    save_jobs(all_jobs)




if __name__ == "__main__":

    collect_jobs()