import pytest
from fastapi.testclient import TestClient
import sys
import os
from dotenv import load_dotenv
# Add the project folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
load_dotenv()
API_KEY = os.getenv("API_KEY")
from main import app

client = TestClient(app)
headers = {
    "accept": "application/json",
    "access_token": API_KEY
}
def test_get_all_users():

    response = client.get("/api/v1/users", headers=headers)
    assert response.status_code == 200
    assert response.json() is not None

def test_get_all_transactions():
    response = client.get("/api/v1/transactions", headers=headers)
    assert response.status_code == 200
    assert response.json() is not None

def test_get_all_products():
    response = client.get("/api/v1/product", headers=headers)
    assert response.status_code == 200
    assert response.json() is not None