import os
import requests
from dotenv import load_dotenv
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.security import APIKeyHeader
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

app = FastAPI()
router_v1 = APIRouter()
# Load environment variables from the .env file
load_dotenv()
# Base URL and access token
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")

API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME)
# Endpoint URLs for user, product, and transaction data
USER_URL = f"{BASE_URL}/users"
PRODUCT_URL = f"{BASE_URL}/products"
TRANSACTION_URL = f"{BASE_URL}/transactions"

# Define headers with access token
headers = {"access_token": API_KEY, "Content-Type": "application/json"}
# Define a mapping for preferences
preference_mapping = {
    "Electronics": 1,
    "Clothing": 2,
    "Sports": 3,
    "Books": 4,
    "Food": 5,
}


# Authenticator function for API key validation
async def get_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return api_key


@router_v1.get("/recommend/{user_id}")
async def get_recommendations(user_id: int, api_key: str = Depends(get_api_key)):
    reader = Reader(rating_scale=(1, 5))
    try:
        # Fetch user data
        user_data = requests.get(USER_URL, headers=headers).json()

        # Fetch product data
        product_data = requests.get(PRODUCT_URL, headers=headers).json()

        # Fetch transaction history
        transaction_data = requests.get(TRANSACTION_URL, headers=headers).json()

        # Extract preferences from user data
        preferences = [user["preferences"] for user in user_data]

        # Initialize label encoder
        label_encoder = LabelEncoder()

        # Convert preferences to numerical form
        numerical_preferences = label_encoder.fit_transform(preferences)

        # Update user data with numerical preferences
        for index, user in enumerate(user_data):
            user["numerical_preferences"] = numerical_preferences[index]

        # Create DataFrames from the fetched data
        user_data_frame = pd.DataFrame(user_data)
        product_data_frame = pd.DataFrame(product_data)
        transaction_data_frame = pd.DataFrame(transaction_data)

        # Merge dataframes based on common columns
        merged_data = pd.merge(user_data_frame, transaction_data_frame, on="user_id")
        final_data = pd.merge(
            merged_data, product_data_frame, left_on="product_id", right_on="product_id"
        )

        data = Dataset.load_from_df(
            final_data[["user_id", "product_id", "numerical_preferences"]], reader
        )

    except Exception as e:
        print(f"Failed to load data from API. Loading data from CSV. Error: {e}")
        final_data = pd.read_csv("dataset.csv")
        final_data["preferences"] = final_data["preferences"].map(preference_mapping)

        # Load data into Surprise (example code)
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(
            final_data[["user_id", "product_id", "preferences"]], reader
        )

    trainset, testset = train_test_split(data, test_size=0.2)
    algo = SVD()
    algo.fit(trainset)
    # Make predictions for the specified user
    user_predictions = []
    for product_id in final_data["product_id"].unique():
        prediction = algo.predict(user_id, product_id)
        user_predictions.append((product_id, prediction.est))

    # Sort the predictions by estimated rating
    sorted_predictions = sorted(user_predictions, key=lambda x: x[1], reverse=True)

    # Return the top recommendations
    top_recommendations = [
        {"product_id": int(product_id), "estimated_rating": est_rating}
        for product_id, est_rating in sorted_predictions[:3]
    ]

    return {"user_id": user_id, "recommendations": top_recommendations}


app.include_router(router_v1, prefix="/api/v1")
