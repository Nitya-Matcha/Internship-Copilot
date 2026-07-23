from database import SessionLocal
from models import Internship


db = SessionLocal()

jobs = [
    Internship(
        company="Capital One",
        title="Software Engineering Intern",
        location="McLean, VA",
        url="https://www.capitalonecareers.com"
    ),

    Internship(
        company="NVIDIA",
        title="Software Engineering Intern",
        location="Santa Clara, CA",
        url="https://www.nvidia.com/careers"
    ),

    Internship(
        company="Amazon",
        title="Software Development Engineer Intern",
        location="Seattle, WA",
        url="https://www.amazon.jobs"
    )
]


db.add_all(jobs)
db.commit()

db.close()

print("Internships added!")