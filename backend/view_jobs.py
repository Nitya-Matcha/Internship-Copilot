from database import SessionLocal
from models import Job

db = SessionLocal()

jobs = db.query(Job).all()

for job in jobs:
    print("----------------")
    print(job.company)
    print(job.title)
    print(job.skills)

db.close()