"""
Career Counseling Agent
Autonomous agentic loop that:
1. Reads student academic profile & assessment scores
2. Fetches labor market trends
3. Calls IBM Granite to synthesize personalized career pathways
4. Stores results and returns structured recommendations
"""

import logging
import json
from typing import Any
from datetime import datetime

from services.granite_service import generate_text

logger = logging.getLogger(__name__)


# ── Prompt Templates ─────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert AI career counselor with deep knowledge of:
- Academic performance analysis and skill gap identification
- Global and regional labor market trends
- Career pathway planning across STEM, Arts, Business, Healthcare, and Law
- Industry certifications, internship programs, and higher education options

Your role is to provide data-driven, empathetic, and actionable career guidance
tailored to each student's unique strengths, interests, and goals.
Always be encouraging, specific, and realistic about career timelines.
"""

CAREER_RECOMMENDATION_PROMPT = """
{system}

## Student Profile
- Name: {name}
- Grade/Year: {grade_level}
- Field of Study: {field_of_study}
- GPA: {gpa}
- Interests: {interests}
- Skills: {skills}
- Extracurricular Activities: {extracurriculars}
- Preferred Work Style: {work_style}
- Location Preference: {location}

## Academic Performance (Recent)
{academic_records}

## Assessment Results
- Interest Profile: {interest_scores}
- Aptitude Profile: {aptitude_scores}
- Personality Traits: {personality_scores}

## Current Labor Market Context
{market_context}

## Task
Based on the above comprehensive student profile, provide:

1. **Top 3 Recommended Career Pathways** — for each career include:
   - Career title and brief description
   - Why it suits this student (link to their specific strengths)
   - Required skills/qualifications they already have vs. gaps to fill
   - 5-year salary range and growth outlook
   - Top companies/sectors hiring for this role

2. **Personalized Action Plan** — 6 concrete, time-bound steps the student should take
   in the next 12 months to progress toward their top career choice.

3. **Skills Gap Analysis** — identify 3 key skills to develop and recommend
   specific resources (courses, certifications, projects).

4. **Alternative Pathways** — mention 2 backup options that leverage their strengths.

5. **Motivational Summary** — a brief, encouraging closing note (2-3 sentences).

Be specific, practical, and base your reasoning on the data provided.
"""

CHAT_PROMPT = """
{system}

## Student Context
{student_context}

## Conversation History
{history}

## Student's Current Question
{question}

## Response
Provide a helpful, personalized, and encouraging response.
"""


class CareerCounselingAgent:
    """
    Agentic orchestrator that drives the career counseling workflow.
    """

    def __init__(self):
        self.generate = generate_text

    # ─────────────────────────────────────────────────────────
    #  Public Methods
    # ─────────────────────────────────────────────────────────

    def generate_career_plan(self, student_data: dict, market_data: dict) -> dict:
        """
        Main agentic method: synthesizes all available data
        and calls IBM Granite to produce a career plan.
        """
        logger.info(f"Generating career plan for student: {student_data.get('name')}")

        prompt = self._build_recommendation_prompt(student_data, market_data)
        raw_response = self.generate(prompt)

        plan = self._parse_career_plan(raw_response)
        plan["generated_at"] = datetime.utcnow().isoformat()
        plan["model"] = "ibm/granite-3-8b-instruct"
        plan["raw_response"] = raw_response

        logger.info("Career plan generated successfully.")
        return plan

    def chat(self, question: str, student_context: dict, history: list) -> str:
        """
        Conversational career counseling — answers student questions
        in context of their profile and prior conversation.
        """
        history_text = self._format_history(history[-6:])  # last 6 exchanges
        context_text = self._format_student_context(student_context)

        prompt = CHAT_PROMPT.format(
            system=SYSTEM_PROMPT,
            student_context=context_text,
            history=history_text,
            question=question,
        )
        return self.generate(prompt)

    def analyze_skills_gap(self, student_data: dict, target_career: str) -> dict:
        """
        Focused analysis of skill gaps for a specific target career.
        """
        prompt = f"""
{SYSTEM_PROMPT}

## Student Profile
- Skills: {student_data.get('skills', [])}
- Academic Strengths: {student_data.get('strong_subjects', [])}
- GPA: {student_data.get('gpa', 'N/A')}

## Target Career: {target_career}

Provide a detailed skill gap analysis:
1. Skills the student already has that apply
2. Critical missing skills (top 5)
3. Recommended learning resources for each gap
4. Estimated time to close each gap
5. Overall readiness score (0-100)

Be specific and actionable.
"""
        response = self.generate(prompt)
        return {"career": target_career, "analysis": response}

    # ─────────────────────────────────────────────────────────
    #  Private Helpers
    # ─────────────────────────────────────────────────────────

    def _build_recommendation_prompt(self, student: dict, market: dict) -> str:
        academic_records = self._format_academic_records(
            student.get("academic_records", [])
        )
        market_context = self._format_market_context(market)

        assessment = student.get("assessment", {})
        return CAREER_RECOMMENDATION_PROMPT.format(
            system=SYSTEM_PROMPT,
            name=student.get("name", "Student"),
            grade_level=student.get("grade_level", "N/A"),
            field_of_study=student.get("field_of_study", "N/A"),
            gpa=student.get("gpa", "N/A"),
            interests=", ".join(student.get("interests", [])) or "Not specified",
            skills=", ".join(student.get("skills", [])) or "Not specified",
            extracurriculars=", ".join(student.get("extracurriculars", [])) or "None listed",
            work_style=student.get("preferred_work_style", "Flexible"),
            location=student.get("location_preference", "Open"),
            academic_records=academic_records,
            interest_scores=json.dumps(assessment.get("interest_scores", {}), indent=2),
            aptitude_scores=json.dumps(assessment.get("aptitude_scores", {}), indent=2),
            personality_scores=json.dumps(assessment.get("personality_scores", {}), indent=2),
            market_context=market_context,
        )

    def _format_academic_records(self, records: list) -> str:
        if not records:
            return "No academic records available."
        lines = []
        for r in records:
            lines.append(
                f"- {r.get('subject', '?')}: {r.get('grade', '?')} "
                f"(Score: {r.get('score', '?')}) — {r.get('semester', '')} {r.get('academic_year', '')}"
            )
        return "\n".join(lines)

    def _format_market_context(self, market: dict) -> str:
        if not market:
            return "Real-time market data unavailable. Using general trends."
        trends = market.get("trends", [])
        hot_roles = market.get("hot_roles", [])
        return (
            f"Top trending sectors: {', '.join(trends[:5])}\n"
            f"High-demand roles: {', '.join(hot_roles[:5])}\n"
            f"Overall market sentiment: {market.get('sentiment', 'Positive')}"
        )

    def _format_student_context(self, ctx: dict) -> str:
        return (
            f"Name: {ctx.get('name', 'Student')}, "
            f"Field: {ctx.get('field_of_study', 'N/A')}, "
            f"GPA: {ctx.get('gpa', 'N/A')}, "
            f"Interests: {', '.join(ctx.get('interests', []))}"
        )

    def _format_history(self, history: list) -> str:
        if not history:
            return "No prior conversation."
        return "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in history
        )

    def _parse_career_plan(self, raw: str) -> dict:
        """
        Lightly structures the raw Granite response.
        A production system would use structured output / JSON mode.
        """
        sections = raw.split("\n\n")
        return {
            "recommended_careers": self._extract_section(raw, "Career Pathway", limit=3),
            "action_steps": self._extract_section(raw, "Action Plan", limit=6),
            "skills_gap": self._extract_section(raw, "Skills Gap", limit=5),
            "alternative_pathways": self._extract_section(raw, "Alternative", limit=2),
            "summary": sections[-1] if sections else raw,
            "full_plan": raw,
        }

    def _extract_section(self, text: str, keyword: str, limit: int) -> list:
        lines = text.split("\n")
        collecting = False
        items = []
        for line in lines:
            if keyword.lower() in line.lower():
                collecting = True
                continue
            if collecting:
                stripped = line.strip("-•*1234567890. \t")
                if stripped and len(stripped) > 10:
                    items.append(stripped)
                if len(items) >= limit:
                    break
        return items


# Singleton instance
career_agent = CareerCounselingAgent()
