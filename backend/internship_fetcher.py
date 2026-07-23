from database import SessionLocal
from models import Internship


def add_job(company, title, location, url):

    db = SessionLocal()

    job = Internship(
        company=company,
        title=title,
        location=location,
        url=url
    )

    db.add(job)
    db.commit()
    db.close()