import sys
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
csv_file = os.path.join(current_dir, 'dataset.csv')
# Read data from CSV
data = pd.read_csv(csv_file)
data.drop_duplicates(subset=['product_id'], keep='first', inplace=True)
from db.database import engine
from models.product import Product
# Iterate through each row and insert into the Product table
# Create a session
Session = sessionmaker(bind=engine)
session = Session()
for _, row in data.iterrows():
    product = Product(
        product_id=row['product_id'],
        category=row['category'],
        Product_name=row['Product_name'],
        description=row['description'],
        tags=row['tags']
    )
    session.add(product)

# Commit the changes
session.commit()

# Close the session
session.close()

print("Data inserted into Product table successfully.")
