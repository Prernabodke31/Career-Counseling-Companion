"""
Assessment Routes
Handles interest, aptitude, and personality assessments.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, List

from database import get_db
from models.models import User, Assessment
from services.auth_service import get_current_user

router = APIRouter()


# ── Assessment Questions Bank ─────────────────────────────────

ASSESSMENT_QUESTIONS = {
    "interest": [
        {"id": "i1", "question": "I enjoy solving complex logical puzzles.", "dimension": "analytical"},
        {"id": "i2", "question": "I like working with computers and technology.", "dimension": "technical"},
        {"id": "i3", "question": "I enjoy helping or teaching others.", "dimension": "social"},
        {"id": "i4", "question": "I like creating art, music, or writing.", "dimension": "creative"},
        {"id": "i5", "question": "I enjoy leading teams and making decisions.", "dimension": "leadership"},
        {"id": "i6", "question": "I'm interested in how the body and health work.", "dimension": "medical"},
        {"id": "i7", "question": "I like organizing data and working with numbers.", "dimension": "quantitative"},
        {"id": "i8", "question": "I enjoy reading about business and economics.", "dimension": "business"},
        {"id": "i9", "question": "I care about environmental and social issues.", "dimension": "humanitarian"},
        {"id": "i10", "question": "I enjoy research and discovering new knowledge.", "dimension": "research"},
    ],
    "aptitude": [
        {"id": "a1", "question": "I can easily understand technical manuals.", "dimension": "technical_reasoning"},
        {"id": "a2", "question": "I excel at mental math and numerical analysis.", "dimension": "numerical"},
        {"id": "a3", "question": "I communicate ideas clearly in writing.", "dimension": "verbal"},
        {"id": "a4", "question": "I can visualize 3D objects from 2D diagrams.", "dimension": "spatial"},
        {"id": "a5", "question": "I quickly adapt to new software and tools.", "dimension": "digital_literacy"},
        {"id": "a6", "question": "I can identify patterns in data sets.", "dimension": "analytical"},
        {"id": "a7", "question": "I work well under time pressure.", "dimension": "stress_tolerance"},
        {"id": "a8", "question": "I can manage multiple tasks simultaneously.", "dimension": "multitasking"},
    ],
    "personality": [
        {"id": "p1", "question": "I prefer working in a team over working alone.", "dimension": "extroversion"},
        {"id": "p2", "question": "I enjoy routine and structured environments.", "dimension": "structure_preference"},
        {"id": "p3", "question": "I am comfortable with ambiguity and change.", "dimension": "adaptability"},
        {"id": "p4", "question": "I tend to plan ahead before starting a project.", "dimension": "conscientiousness"},
        {"id": "p5", "question": "I empathize easily with others' feelings.", "dimension": "empathy"},
        {"id": "p6", "question": "I enjoy taking risks for potential rewards.", "dimension": "risk_tolerance"},
        {"id": "p7", "question": "I prefer deep expertise in one area over broad knowledge.", "dimension": "specialization"},
        {"id": "p8", "question": "I am motivated by recognition and achievement.", "dimension": "achievement_drive"},
    ],
}

# Likert scale: 1 = Strongly Disagree, 5 = Strongly Agree


# ── Schemas ───────────────────────────────────────────────────

class AssessmentSubmit(BaseModel):
    assessment_type: str        # interest | aptitude | personality
    responses: Dict[str, int]   # question_id -> score (1–5)


# ── Endpoints ─────────────────────────────────────────────────

@router.get("/questions/{assessment_type}")
def get_questions(assessment_type: str):
    if assessment_type not in ASSESSMENT_QUESTIONS:
        return {"error": f"Unknown assessment type. Choose: {list(ASSESSMENT_QUESTIONS.keys())}"}
    return {
        "type": assessment_type,
        "scale": "1 (Strongly Disagree) to 5 (Strongly Agree)",
        "questions": ASSESSMENT_QUESTIONS[assessment_type],
    }


@router.post("/submit", status_code=201)
def submit_assessment(
    payload: AssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    questions = ASSESSMENT_QUESTIONS.get(payload.assessment_type, [])
    scores: Dict[str, float] = {}

    for q in questions:
        resp_value = payload.responses.get(q["id"], 3)
        dim = q["dimension"]
        scores[dim] = scores.get(dim, 0) + resp_value

    # Normalize to 0–100
    max_per_dim = 5
    normalized = {dim: round((val / max_per_dim) * 100, 1) for dim, val in scores.items()}
    top_dim = max(normalized, key=normalized.get) if normalized else "general"

    summary = (
        f"Your strongest {payload.assessment_type} dimension is '{top_dim}' "
        f"(score: {normalized.get(top_dim, 0)}/100). "
        f"Full breakdown: {normalized}"
    )

    assessment = Assessment(
        student_id=current_user.id,
        assessment_type=payload.assessment_type,
        responses=payload.responses,
        scores=normalized,
        summary=summary,
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return {
        "message": "Assessment submitted successfully.",
        "assessment_id": assessment.id,
        "scores": normalized,
        "top_dimension": top_dim,
        "summary": summary,
    }


@router.get("/history")
def get_assessment_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    assessments = (
        db.query(Assessment)
        .filter(Assessment.student_id == current_user.id)
        .order_by(Assessment.taken_at.desc())
        .all()
    )
    return [
        {
            "id": a.id,
            "type": a.assessment_type,
            "scores": a.scores,
            "summary": a.summary,
            "taken_at": a.taken_at,
        }
        for a in assessments
    ]
