from database import SessionLocal
from models import Job


def clear_jobs():

    db = SessionLocal()

    deleted = db.query(Job).delete()

    db.commit()
    db.close()

    print(f"Deleted {deleted} jobs")


if __name__ == "__main__":
    clear_jobs()