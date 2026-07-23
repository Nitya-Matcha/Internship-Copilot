from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

Base = declarative_base()


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
