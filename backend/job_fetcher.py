import requests
from database import SessionLocal
from models import Internship


def fetch_greenhouse_jobs(company):

    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    jobs = []

    for job in data["jobs"]:

        jobs.append({
            "company": company,
            "title": job["title"],
            "location": job["location"]["name"],
            "url": job["absolute_url"]
        })

    return jobs


def save_jobs(jobs):

    db = SessionLocal()

    for job in jobs:

        existing = db.query(Internship).filter(
            Internship.url == job["url"]
        ).first()

        if not existing:

            internship = Internship(
                company=job["company"],
                title=job["title"],
                location=job["location"],
                url=job["url"]
            )

            db.add(internship)

    db.commit()
    db.close()


if __name__ == "__main__":

    companies = [
        "nvidia",
        "capitalone",
        "stripe"
    ]

    all_jobs = []

    for company in companies:
        jobs = fetch_greenhouse_jobs(company)
        all_jobs.extend(jobs)

    save_jobs(all_jobs)

    print(f"Added {len(all_jobs)} internships")