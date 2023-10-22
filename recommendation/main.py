import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException,Depends, status, APIRouter
from fastapi.security import APIKeyHeader
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import LabelEncoder


app = FastAPI()
router_v1 = APIRouter()
# Load environment variables from the .env file
load_dotenv()
# Base URL and access token
BASE_URL =  os.getenv("BASE_URL")
API_KEY =  os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")

API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME)
# Endpoint URLs for user, product, and transaction data
user_url = f"{BASE_URL}/users"
product_url = f"{BASE_URL}/products"
transaction_url = f"{BASE_URL}/transactions"

# Define headers with access token
headers = {
    "access_token": API_KEY,
    "Content-Type": "application/json"
}

# Assuming 'final_df' is the DataFrame containing the user preferences and purchase history
# 'final_df' should have 'user_id', 'product_id', and 'rating' columns

# Authenticator function for API key validation
async def get_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return api_key

@router_v1.get("/recommend/{user_id}")
async def get_recommendations(user_id: int,api_key: str = Depends(get_api_key)):
    reader = Reader(rating_scale=(1, 5))

    # Fetch user data
    user_data = requests.get(user_url, headers=headers).json()

    # Fetch product data
    product_data = requests.get(product_url, headers=headers).json()

    # Fetch transaction history
    transaction_data = requests.get(transaction_url, headers=headers).json()

    
    # Extract preferences from user data
    preferences = [user['preferences'] for user in user_data]
   
    # Initialize label encoder
    label_encoder = LabelEncoder()

    # Convert preferences to numerical form
    numerical_preferences = label_encoder.fit_transform(preferences)


    # Update user data with numerical preferences
    for index, user in enumerate(user_data):
        user['numerical_preferences'] = numerical_preferences[index]


    # Create DataFrames from the fetched data
    user_df = pd.DataFrame(user_data)
    product_df = pd.DataFrame(product_data)
    transaction_df = pd.DataFrame(transaction_data)

    # Merge dataframes based on common columns
    merged_df = pd.merge(user_df, transaction_df, on='user_id')
    final_df = pd.merge(merged_df, product_df, left_on='product_id', right_on='product_id')

    data = Dataset.load_from_df(final_df[['user_id', 'product_id', 'numerical_preferences']], reader)
 
    # Split the data into training and testing sets
    trainset, testset = train_test_split(data, test_size=0.2)

    # Use the SVD algorithm
    algo = SVD()

    # Train the algorithm on the training set
    algo.fit(trainset)
 
    # Make predictions for the specified user
    user_predictions = []
    for product_id in final_df['product_id'].unique():
        prediction = algo.predict(user_id, product_id)
        user_predictions.append((product_id, prediction.est))

    # Sort the predictions by estimated rating
    sorted_predictions = sorted(user_predictions, key=lambda x: x[1], reverse=True)
    
    # Return the top recommendations
    top_recommendations = [{"product_id": int(product_id), "estimated_rating": est_rating} for product_id, est_rating in sorted_predictions[:3]]

    return {"user_id": user_id, "recommendations": top_recommendations}

app.include_router(router_v1, prefix="/api/v1")

# if __name__ == "__main__":
#     import uvicorn
#     # uvicorn.run(app, host="0.0.0.0", port=5000)
#     uvicorn.run(app, host="127.0.0.1", port=5000)
