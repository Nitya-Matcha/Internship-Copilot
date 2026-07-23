from sqlalchemy import Column, Integer, String, Text
from database import Base


class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True)
    company = Column(String)
    title = Column(String)
    location = Column(String)
    url = Column(String, unique=True)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    resume_text = Column(Text)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)

    company = Column(String)
    title = Column(String)
    url = Column(String)

    status = Column(String)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String, nullable=False)

    title = Column(String, nullable=False)

    location = Column(String)

    url = Column(String, nullable=False, unique=True)

    skills = Column(String)