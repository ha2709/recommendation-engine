import sys
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
csv_file = os.path.join(current_dir, 'dataset.csv')

from models.user import User
from db.database import Base, engine
# Create a session
Session = sessionmaker(bind=engine)
session = Session()
def read_csv_insert_to_user_table(csv_file):
    try:
        # Read data from CSV
        data = pd.read_csv(csv_file)
        # Remove duplicates based on 'user_id'
        data.drop_duplicates(subset=['user_id'], keep='first', inplace=True)
        # Create MySQL connection
        Base.metadata.create_all(engine)

        # Insert data into the User table
        for _, row in data.iterrows():
            user = User(
                user_id=row['user_id'],
                name=row['name'],
                age=row['age'],
                gender=row['gender'],
                location=row['location'],
                preferences=row['preferences']
            )

            session.add(user)
        session.commit()

        print("Data inserted into User table successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

read_csv_insert_to_user_table(csv_file)
