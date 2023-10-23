# import unittest
# from unittest.mock import patch
# import asyncio
# import importlib.util

# spec = importlib.util.spec_from_file_location("services", "services.py")
# services = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(services)

# class TestRecommendationService(unittest.TestCase):

#     @patch('services.requests.get')
#     def test_get_recommendations(self, mock_get):
#         async def async_mock_get(*args, **kwargs):
#             mock_response = {
#                 "users": [{"id": 102, "preferences": "Electronics"}],
#                 "products": [{"id": 105, "name": "Product A"}, {"id": 102, "name": "Product B"}, {"id": 103, "name": "Product C"}],
#                 "transactions": [{"user_id": 102, "product_id": 105, "transaction_id": 1},
#                                  {"user_id": 102, "product_id": 102, "transaction_id": 2},
#                                  {"user_id": 102, "product_id": 103, "transaction_id": 3}]
#             }
#             return mock_response

#         mock_get.side_effect = async_mock_get

#         async def run_test():
#             recommendation_service = services.RecommendationService()
#             result = await recommendation_service.get_recommendations(102, "valid_api_key")

#             self.assertEqual(result["user_id"], 102)
#             self.assertEqual(len(result["recommendations"]), 3)

#             ratings = [res["estimated_rating"] for res in result["recommendations"]]
#             self.assertEqual(len(set(ratings)), len(ratings))  # Check if all estimated ratings are unique

#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(run_test())

# if __name__ == '__main__':
#     unittest.main()


# import importlib.util

# spec = importlib.util.spec_from_file_location("services", "services.py")
# services = importlib.util.module_from_spec(spec)
import sys
import os
 
from dotenv import load_dotenv
import pytest
import asyncio
load_dotenv()
# Add the path to the directory containing services.py to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services import RecommendationService

@pytest.mark.asyncio
async def test_get_recommendations():
    service = RecommendationService()
    user_id = 102
    API_KEY =  os.getenv("API_KEY") # Assuming the API key is valid for testing purposes

    result = await service.get_recommendations(user_id, API_KEY)

    assert "user_id" in result
    assert len(result["recommendations"]) == 3
    assert all(isinstance(rec['product_id'], int) for rec in result["recommendations"])
    assert all(isinstance(rec['estimated_rating'], float) for rec in result["recommendations"])

    # Check that estimated ratings are different per request
    estimated_ratings = [rec['estimated_rating'] for rec in result["recommendations"]]
    assert len(set(estimated_ratings)) == len(estimated_ratings)  # All ratings are unique
