"""
IBM Granite Service
Connects to IBM WatsonX.ai and provides text generation
via the ibm-watsonx-ai SDK and LangChain integration.
"""

import logging
from typing import Optional
from functools import lru_cache

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_granite_model() -> ModelInference:
    """
    Returns a cached IBM Granite ModelInference instance.
    Uses IBM WatsonX credentials from .env
    """
    credentials = Credentials(
        url=settings.IBM_WATSONX_URL,
        api_key=settings.IBM_WATSONX_API_KEY,
    )
    model = ModelInference(
        model_id=settings.IBM_GRANITE_MODEL_ID,
        credentials=credentials,
        project_id=settings.IBM_WATSONX_PROJECT_ID,
        params={
            GenParams.MAX_NEW_TOKENS: 1024,
            GenParams.MIN_NEW_TOKENS: 50,
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_P: 0.95,
            GenParams.TOP_K: 50,
            GenParams.REPETITION_PENALTY: 1.1,
        },
    )
    logger.info(f"IBM Granite model initialized: {settings.IBM_GRANITE_MODEL_ID}")
    return model


def generate_text(prompt: str, max_tokens: int = 1024) -> str:
    """
    Send a prompt to IBM Granite and return the generated text.
    Falls back to a mock response if credentials are not configured.
    """
    # ── Mock mode when no credentials configured ─────────────
    if not settings.IBM_WATSONX_API_KEY or settings.IBM_WATSONX_API_KEY == "your_ibm_watsonx_api_key_here":
        logger.warning("IBM WatsonX API key not set — using mock response.")
        return _mock_response(prompt)

    try:
        model = get_granite_model()
        response = model.generate_text(prompt=prompt)
        return response
    except Exception as exc:
        logger.error(f"Granite generation error: {exc}")
        return _mock_response(prompt)


def _mock_response(prompt: str) -> str:
    """
    Demo mock when IBM credentials are absent.
    Returns realistic-sounding placeholder text.
    """
    if "career" in prompt.lower() or "recommend" in prompt.lower():
        return (
            "Based on your academic strengths and interests, here are your top career pathways:\n\n"
            "1. **Software Engineer / Full-Stack Developer** — Your strong performance in Mathematics "
            "and Computer Science, combined with problem-solving aptitude, makes this an excellent fit. "
            "The tech sector shows 15% projected growth over the next 5 years.\n\n"
            "2. **Data Scientist / AI Engineer** — Your analytical skills and curiosity about patterns "
            "align well with data roles. IBM, Google, and Microsoft are actively hiring.\n\n"
            "3. **Product Manager (Tech)** — Your blend of technical knowledge and communication skills "
            "positions you for leadership roles bridging engineering and business.\n\n"
            "**Recommended Action Steps:**\n"
            "- Complete a Python or Java certification (Coursera / IBM SkillsBuild)\n"
            "- Build 2-3 portfolio projects on GitHub\n"
            "- Apply for summer internships at IBM, Infosys, or TCS\n"
            "- Join IEEE or ACM student chapters for networking\n\n"
            "The labor market outlook for technology roles in your region is **strong**, "
            "with median salaries ranging from $85,000–$130,000 USD annually."
        )
    return (
        "I'm your AI career counselor powered by IBM Granite. "
        "Tell me about your academic background and interests, "
        "and I'll provide personalized career pathway recommendations."
    )
