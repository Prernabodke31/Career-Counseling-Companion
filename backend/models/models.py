"""
SQLAlchemy ORM Models
"""

from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean,
    DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="student")   # student | counselor | admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    profile = relationship("StudentProfile", back_populates="user", uselist=False)
    assessments = relationship("Assessment", back_populates="student")
    career_plans = relationship("CareerPlan", back_populates="student")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    grade_level = Column(String)          # e.g. "10th", "Undergraduate Year 2"
    field_of_study = Column(String)
    gpa = Column(Float)
    interests = Column(JSON)              # list of strings
    skills = Column(JSON)                 # list of strings
    extracurriculars = Column(JSON)       # list of strings
    preferred_work_style = Column(String) # remote / hybrid / on-site
    location_preference = Column(String)
    bio = Column(Text)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship("User", back_populates="profile")
    academic_records = relationship("AcademicRecord", back_populates="profile")


class AcademicRecord(Base):
    __tablename__ = "academic_records"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id"))
    subject = Column(String, nullable=False)
    grade = Column(String)          # A, B+, 85, etc.
    score = Column(Float)           # numeric 0-100
    semester = Column(String)
    academic_year = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    profile = relationship("StudentProfile", back_populates="academic_records")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    assessment_type = Column(String)   # interest | aptitude | personality
    responses = Column(JSON)           # question_id -> answer
    scores = Column(JSON)              # dimension -> score dict
    summary = Column(Text)
    taken_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("User", back_populates="assessments")


class CareerPlan(Base):
    __tablename__ = "career_plans"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    recommended_careers = Column(JSON)   # list of career dicts
    reasoning = Column(Text)             # Granite-generated explanation
    action_steps = Column(JSON)          # list of step strings
    market_outlook = Column(JSON)        # job market snapshot
    confidence_score = Column(Float)     # 0.0 – 1.0
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    student = relationship("User", back_populates="career_plans")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    messages = Column(JSON)   # list of {role, content, timestamp}
    session_name = Column(String, default="Career Chat")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
