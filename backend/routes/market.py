"""
Labor Market Routes
Exposes market intelligence and live job listings.
"""

from fastapi import APIRouter, Query
from services.market_service import market_service

router = APIRouter()


@router.get("/overview")
async def market_overview():
    """Returns current labor market overview and trending sectors."""
    data = await market_service.get_market_overview()
    return data


@router.get("/jobs")
async def job_listings(
    role: str = Query("Software Engineer", description="Job role to search for"),
    location: str = Query("Remote", description="Preferred location"),
):
    """Returns live job listings for a given role and location."""
    jobs = await market_service.get_job_listings(role=role, location=location)
    return {"role": role, "location": location, "listings": jobs, "count": len(jobs)}


@router.get("/in-demand-skills")
async def in_demand_skills():
    """Returns the top skills currently in demand across the job market."""
    data = await market_service.get_market_overview()
    return {
        "top_skills": data.get("top_skills_in_demand", []),
        "source": data.get("source", "N/A"),
        "last_updated": data.get("last_updated", "N/A"),
    }


@router.get("/salary/{role}")
async def salary_info(role: str):
    """Returns salary range information for a specific role."""
    data = await market_service.get_market_overview()
    salary_ranges = data.get("salary_ranges", {})

    # Case-insensitive match
    for key, val in salary_ranges.items():
        if role.lower() in key.lower() or key.lower() in role.lower():
            return {"role": key, "salary": val, "source": data.get("source")}

    return {
        "role": role,
        "salary": {"note": "Specific data not available. Check LinkedIn Salary or Glassdoor."},
        "all_available": list(salary_ranges.keys()),
    }
