from database import SessionLocal
from models import Internship, Application


def get_all_internships():

    db = SessionLocal()

    internships = db.query(Internship).all()

    results = []

    for job in internships:
        results.append({
            "id": job.id,
            "company": job.company,
            "title": job.title,
            "location": job.location,
            "url": job.url
        })

    db.close()

    return results