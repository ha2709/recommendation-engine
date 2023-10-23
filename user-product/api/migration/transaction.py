import sys
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
csv_file = os.path.join(current_dir, 'dataset.csv')
from db.database import engine
from models.transactions import Transaction

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Read data from CSV
data = pd.read_csv(csv_file)

# Iterate through each row and insert into the Transaction table
for number, row in data.iterrows():
    transaction = Transaction(
        transaction_id=number +1,
        user_id=int(row['user_id']),
        product_id=int(row['product_id'])
    )
    session.add(transaction)

# Commit the changes
session.commit()

# Close the session
session.close()

print("Data inserted into Transaction table successfully.")
