import sys
import os
import asyncio
from dotenv import load_dotenv
import pytest

load_dotenv()
# Add the path to the directory containing services.py to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services import RecommendationService


@pytest.mark.asyncio
async def test_get_recommendations():
    service = RecommendationService()
    user_id = 102
    API_KEY = os.getenv("API_KEY")  # Assuming the API key is valid for testing purposes

    result = await service.get_recommendations(user_id, API_KEY)

    assert "user_id" in result
    assert len(result["recommendations"]) == 3
    assert all(isinstance(rec["product_id"], int) for rec in result["recommendations"])
    assert all(
        isinstance(rec["estimated_rating"], float) for rec in result["recommendations"]
    )

    # Check that estimated ratings are different per request
    estimated_ratings = [rec["estimated_rating"] for rec in result["recommendations"]]
    assert len(set(estimated_ratings)) == len(
        estimated_ratings
    )  # All ratings are unique
