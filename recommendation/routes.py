import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from services import RecommendationService


load_dotenv()
router_v1 = APIRouter()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME)

recommendation_service = RecommendationService()

@router_v1.get("/recommend/{user_id}")
async def get_recommendations(user_id: int, api_key: str = Depends(API_KEY_HEADER)):
    result = await recommendation_service.get_recommendations(user_id, api_key)
    return result
