from database import SessionLocal
from job_collector import collect_jobs
from models import Job

db = SessionLocal()

try:
    jobs = collect_jobs()

    for job in jobs:

        existing = (
            db.query(Job)
            .filter(Job.url == job["url"])
            .first()
        )

        if existing:
            continue

        db.add(
            Job(
                company=job["company"],
                title=job["title"],
                location=job["location"],
                url=job["url"],
                skills=job["skills"]
            )
        )

    db.commit()

    print(f"Added {len(jobs)} jobs")

finally:
    db.close()