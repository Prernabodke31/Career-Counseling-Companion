"""
Labor Market Intelligence Service
Fetches and analyzes real-time job market trends.
Uses JSearch API (via RapidAPI) with a curated fallback dataset.
"""

import logging
import httpx
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)

# ── Curated fallback market data ─────────────────────────────
FALLBACK_MARKET_DATA = {
    "trends": [
        "Artificial Intelligence & Machine Learning",
        "Cybersecurity",
        "Cloud Computing",
        "Data Science & Analytics",
        "Renewable Energy & GreenTech",
        "Biotechnology & Genomics",
        "Digital Health & Telemedicine",
        "FinTech & Blockchain",
        "AR/VR & Metaverse",
        "Supply Chain & Logistics Tech",
    ],
    "hot_roles": [
        "AI/ML Engineer",
        "Data Scientist",
        "Cloud Architect",
        "Cybersecurity Analyst",
        "Full-Stack Developer",
        "DevOps Engineer",
        "Product Manager",
        "UX/UI Designer",
        "Business Intelligence Analyst",
        "Robotics Engineer",
    ],
    "declining_roles": [
        "Data Entry Clerk",
        "Telemarketer",
        "Travel Agent",
        "Print Journalist",
        "Assembly Line Worker",
    ],
    "top_hiring_companies": [
        "IBM", "Google", "Microsoft", "Amazon", "Meta",
        "Deloitte", "Accenture", "TCS", "Infosys", "Wipro",
    ],
    "sentiment": "Positive — Technology sector leads growth",
    "salary_ranges": {
        "Software Engineer": {"min": 80000, "max": 160000, "currency": "USD"},
        "Data Scientist": {"min": 90000, "max": 150000, "currency": "USD"},
        "Cybersecurity Analyst": {"min": 75000, "max": 140000, "currency": "USD"},
        "Product Manager": {"min": 100000, "max": 180000, "currency": "USD"},
        "Cloud Architect": {"min": 110000, "max": 190000, "currency": "USD"},
    },
    "growth_rates": {
        "AI/ML": "40% by 2030",
        "Cybersecurity": "32% by 2030",
        "Data Science": "28% by 2030",
        "Cloud Computing": "25% by 2030",
        "Software Development": "22% by 2030",
    },
    "top_skills_in_demand": [
        "Python", "Cloud (AWS/Azure/GCP)", "Machine Learning",
        "SQL & Data Analysis", "Kubernetes/Docker",
        "React/Node.js", "Cybersecurity Fundamentals",
        "Communication & Leadership", "Project Management (Agile/Scrum)",
        "GenAI & Prompt Engineering",
    ],
    "education_pathways": {
        "Computer Science": ["B.Tech/B.Sc CS", "M.Tech AI/ML", "IBM SkillsBuild Certifications"],
        "Business": ["BBA/MBA", "CFA", "PMP", "Google Digital Marketing"],
        "Healthcare": ["MBBS/Nursing", "Public Health MPH", "Health Informatics"],
        "Engineering": ["B.Tech EE/ME/Civil", "M.Tech Robotics", "PE License"],
    },
    "source": "Curated Market Intelligence (Fallback)",
    "last_updated": "2025-Q4",
}


class MarketIntelligenceService:
    """
    Fetches real-time labor market trends from JSearch API
    and enriches with sector analysis.
    """

    async def get_market_overview(self, query: str = "technology jobs") -> dict:
        """
        Returns market overview — live data preferred, fallback on failure.
        """
        if settings.RAPID_API_KEY:
            try:
                data = await self._fetch_jsearch(query)
                if data:
                    return self._enrich(data)
            except Exception as exc:
                logger.warning(f"JSearch API failed: {exc} — using fallback.")

        return FALLBACK_MARKET_DATA

    async def get_job_listings(self, role: str, location: str = "Remote") -> list:
        """
        Returns job listings for a specific role.
        """
        if not settings.RAPID_API_KEY:
            return self._sample_listings(role)

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    "https://jsearch.p.rapidapi.com/search",
                    headers={
                        "X-RapidAPI-Key": settings.RAPID_API_KEY,
                        "X-RapidAPI-Host": settings.JSEARCH_API_HOST,
                    },
                    params={"query": f"{role} {location}", "num_pages": "1", "page": "1"},
                )
                resp.raise_for_status()
                jobs = resp.json().get("data", [])
                return [
                    {
                        "title": j.get("job_title"),
                        "company": j.get("employer_name"),
                        "location": j.get("job_city", "Remote"),
                        "salary": j.get("job_salary_period"),
                        "url": j.get("job_apply_link"),
                        "posted": j.get("job_posted_at_datetime_utc"),
                    }
                    for j in jobs[:10]
                ]
        except Exception as exc:
            logger.warning(f"Job listing fetch error: {exc}")
            return self._sample_listings(role)

    async def _fetch_jsearch(self, query: str) -> Optional[dict]:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://jsearch.p.rapidapi.com/search",
                headers={
                    "X-RapidAPI-Key": settings.RAPID_API_KEY,
                    "X-RapidAPI-Host": settings.JSEARCH_API_HOST,
                },
                params={"query": query, "num_pages": "1"},
            )
            resp.raise_for_status()
            return resp.json()

    def _enrich(self, raw: dict) -> dict:
        jobs = raw.get("data", [])
        titles = [j.get("job_title", "") for j in jobs]
        companies = [j.get("employer_name", "") for j in jobs]
        return {
            **FALLBACK_MARKET_DATA,
            "hot_roles": list(set(titles))[:10],
            "top_hiring_companies": list(set(companies))[:10],
            "source": "JSearch API (Live)",
        }

    def _sample_listings(self, role: str) -> list:
        return [
            {"title": f"Junior {role}", "company": "IBM", "location": "Remote",
             "salary": "$80k–$110k", "url": "https://ibm.com/careers", "posted": "2025-06-01"},
            {"title": f"Mid-Level {role}", "company": "Google", "location": "Hybrid",
             "salary": "$110k–$150k", "url": "https://careers.google.com", "posted": "2025-06-03"},
            {"title": f"Senior {role}", "company": "Microsoft", "location": "On-site",
             "salary": "$140k–$180k", "url": "https://careers.microsoft.com", "posted": "2025-06-02"},
        ]


market_service = MarketIntelligenceService()
