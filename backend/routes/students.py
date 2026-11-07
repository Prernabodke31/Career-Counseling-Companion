"""
Student Profile & Academic Records Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database import get_db
from models.models import User, StudentProfile, AcademicRecord
from services.auth_service import get_current_user

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────

class ProfileUpdate(BaseModel):
    grade_level: Optional[str] = None
    field_of_study: Optional[str] = None
    gpa: Optional[float] = None
    interests: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    extracurriculars: Optional[List[str]] = None
    preferred_work_style: Optional[str] = None
    location_preference: Optional[str] = None
    bio: Optional[str] = None


class AcademicRecordIn(BaseModel):
    subject: str
    grade: Optional[str] = None
    score: Optional[float] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None


# ── Endpoints ─────────────────────────────────────────────────

@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    records = db.query(AcademicRecord).filter(AcademicRecord.profile_id == profile.id).all()

    return {
        "user_id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "grade_level": profile.grade_level,
        "field_of_study": profile.field_of_study,
        "gpa": profile.gpa,
        "interests": profile.interests or [],
        "skills": profile.skills or [],
        "extracurriculars": profile.extracurriculars or [],
        "preferred_work_style": profile.preferred_work_style,
        "location_preference": profile.location_preference,
        "bio": profile.bio,
        "academic_records": [
            {
                "id": r.id,
                "subject": r.subject,
                "grade": r.grade,
                "score": r.score,
                "semester": r.semester,
                "academic_year": r.academic_year,
            }
            for r in records
        ],
    }


@router.put("/me")
def update_my_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    for field, value in payload.dict(exclude_none=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return {"message": "Profile updated successfully."}


@router.post("/me/academic-records", status_code=201)
def add_academic_record(
    payload: AcademicRecordIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please set up your profile first.")

    record = AcademicRecord(
        profile_id=profile.id,
        subject=payload.subject,
        grade=payload.grade,
        score=payload.score,
        semester=payload.semester,
        academic_year=payload.academic_year,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": "Academic record added.", "record_id": record.id}


@router.delete("/me/academic-records/{record_id}")
def delete_academic_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    record = db.query(AcademicRecord).filter(
        AcademicRecord.id == record_id,
        AcademicRecord.profile_id == profile.id,
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found.")
    db.delete(record)
    db.commit()
    return {"message": "Record deleted."}
