"""
Career Guidance Routes
Invokes the IBM Granite-powered Career Counseling Agent.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import asyncio

from database import get_db
from models.models import User, StudentProfile, AcademicRecord, Assessment, CareerPlan, ChatSession
from services.auth_service import get_current_user
from services.market_service import market_service
from agents.career_agent import career_agent

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────

class ChatMessage(BaseModel):
    content: str


class SkillsGapRequest(BaseModel):
    target_career: str


# ── Helpers ───────────────────────────────────────────────────

def _build_student_data(user: User, db: Session) -> dict:
    """Assembles all student data needed by the career agent."""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    records = (
        db.query(AcademicRecord)
        .filter(AcademicRecord.profile_id == profile.id)
        .all()
        if profile else []
    )
    latest_assessments = {}
    for atype in ["interest", "aptitude", "personality"]:
        a = (
            db.query(Assessment)
            .filter(Assessment.student_id == user.id, Assessment.assessment_type == atype)
            .order_by(Assessment.taken_at.desc())
            .first()
        )
        if a:
            latest_assessments[f"{atype}_scores"] = a.scores

    return {
        "name": user.full_name,
        "grade_level": profile.grade_level if profile else "N/A",
        "field_of_study": profile.field_of_study if profile else "N/A",
        "gpa": profile.gpa if profile else None,
        "interests": profile.interests or [] if profile else [],
        "skills": profile.skills or [] if profile else [],
        "extracurriculars": profile.extracurriculars or [] if profile else [],
        "preferred_work_style": profile.preferred_work_style if profile else "Flexible",
        "location_preference": profile.location_preference if profile else "Open",
        "academic_records": [
            {"subject": r.subject, "grade": r.grade, "score": r.score,
             "semester": r.semester, "academic_year": r.academic_year}
            for r in records
        ],
        "assessment": latest_assessments,
    }


# ── Endpoints ─────────────────────────────────────────────────

@router.post("/recommend")
async def generate_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Main agentic endpoint: generates personalized career pathway recommendations
    by combining student profile, assessments, and live market data via IBM Granite.
    """
    student_data = _build_student_data(current_user, db)
    market_data = await market_service.get_market_overview()

    plan = career_agent.generate_career_plan(student_data, market_data)

    # Persist the plan
    career_plan = CareerPlan(
        student_id=current_user.id,
        recommended_careers=plan.get("recommended_careers", []),
        reasoning=plan.get("full_plan", ""),
        action_steps=plan.get("action_steps", []),
        market_outlook=market_data.get("growth_rates", {}),
        confidence_score=0.85,
    )
    db.add(career_plan)
    db.commit()
    db.refresh(career_plan)

    return {
        "plan_id": career_plan.id,
        "student_name": current_user.full_name,
        "powered_by": "IBM Granite on WatsonX.ai",
        **plan,
    }


@router.get("/plans")
def get_career_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns all previously generated career plans for the student."""
    plans = (
        db.query(CareerPlan)
        .filter(CareerPlan.student_id == current_user.id)
        .order_by(CareerPlan.generated_at.desc())
        .all()
    )
    return [
        {
            "plan_id": p.id,
            "recommended_careers": p.recommended_careers,
            "action_steps": p.action_steps,
            "market_outlook": p.market_outlook,
            "confidence_score": p.confidence_score,
            "generated_at": p.generated_at,
        }
        for p in plans
    ]


@router.post("/chat")
async def chat_with_counselor(
    payload: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Conversational AI career counselor powered by IBM Granite.
    Maintains session history for context-aware responses.
    """
    student_data = _build_student_data(current_user, db)

    # Load or create chat session
    session = (
        db.query(ChatSession)
        .filter(ChatSession.student_id == current_user.id)
        .order_by(ChatSession.updated_at.desc())
        .first()
    )
    if not session:
        session = ChatSession(student_id=current_user.id, messages=[])
        db.add(session)
        db.flush()

    history = session.messages or []

    # Get AI response
    response = career_agent.chat(
        question=payload.content,
        student_context=student_data,
        history=history,
    )

    # Update history
    from datetime import datetime
    history.append({"role": "user", "content": payload.content, "timestamp": datetime.utcnow().isoformat()})
    history.append({"role": "assistant", "content": response, "timestamp": datetime.utcnow().isoformat()})
    session.messages = history

    db.commit()

    return {
        "response": response,
        "session_id": session.id,
        "powered_by": "IBM Granite",
    }


@router.post("/skills-gap")
def analyze_skills_gap(
    payload: SkillsGapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Analyzes the student's skill gap for a specific target career."""
    student_data = _build_student_data(current_user, db)
    result = career_agent.analyze_skills_gap(student_data, payload.target_career)
    return result


@router.get("/chat/history")
def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.student_id == current_user.id)
        .order_by(ChatSession.updated_at.desc())
        .first()
    )
    if not session:
        return {"messages": []}
    return {"session_id": session.id, "messages": session.messages or []}
