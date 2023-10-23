import os
from dotenv import load_dotenv
import requests
import pandas as pd
from fastapi import  HTTPException, Depends
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
# Load environment variables from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
# Define headers with access token


class RecommendationService:
    def __init__(self):
        self.BASE_URL = os.getenv("BASE_URL")
        self.API_KEY = os.getenv("API_KEY")
        self.USER_URL = f"{self.BASE_URL}/users"
        self.PRODUCT_URL = f"{self.BASE_URL}/products"
        self.TRANSACTION_URL = f"{self.BASE_URL}/transactions"
        self.preference_mapping = {
            "Electronics": 1,
            "Clothing": 2,
            "Sports": 3,
            "Books": 4,
            "Food": 5,
        }
        self.headers ={"access_token": API_KEY, "Content-Type": "application/json"}

    async def get_api_key(self, api_key):
        if api_key != self.API_KEY:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key")
        return api_key

    async def get_recommendations(self, user_id: int, api_key: str = Depends(get_api_key)):
        reader = Reader(rating_scale=(1, 5))
        try:
            # Fetch user data
            user_data = requests.get(self.USER_URL, headers=self.headers).json()

            # Fetch product data
            product_data = requests.get(self.PRODUCT_URL, headers=self.headers).json()

            # Fetch transaction history
            transaction_data = requests.get(self.TRANSACTION_URL, headers=self.headers).json()

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
            final_data["preferences"] = final_data["preferences"].map(self.preference_mapping)

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