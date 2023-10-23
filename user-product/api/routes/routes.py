import os
from dotenv import load_dotenv
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN
from schema.product import ProductSchema, ProductCreate
from schema.user import UserCreate, UserSchema
from schema.transactions import TransactionSchema, TransactionCreate
from db.database import SessionLocal
from models.product import Product
from models.transactions import Transaction
from models.user import User
from services.services import get_session
# Load environment variables from .env
load_dotenv()
router_v1 = APIRouter()
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")


API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME)
# Authenticator function for API key validation
async def get_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return api_key
@router_v1.get("/")
def root():
    return "Hello World"

# Get all Users
@router_v1.get("/users", response_model=List[UserSchema])
def get_all_users(api_key: str = Depends(get_api_key),
                  session: Session = Depends(get_session)):  
    users = session.query(User).all()
 
    return users

# Create a User
@router_v1.post("/user", response_model=UserSchema)
def create_user(user: UserCreate,
                api_key: str = Depends(get_api_key),
                session: Session = Depends(get_session)):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# Get a User
@router_v1.get("/user/{user_id}", response_model=UserSchema)
def read_user(user_id: int,
              api_key: str = Depends(get_api_key),
              session: Session = Depends(get_session)):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# # Update a User
@router_v1.put("/user/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreate,
                api_key: str = Depends(get_api_key),
                session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in user:
        setattr(db_user, var, value)
    session.commit()
    return db_user

# Delete a User
@router_v1.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int,
                api_key: str = Depends(get_api_key),
                session: Session = Depends(get_session)):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return None

# Get all Transactions
@router_v1.get("/transactions", response_model=List[TransactionSchema])
def get_all_transactions( api_key: str = Depends(get_api_key),
                          session: Session = Depends(get_session)): 
    transactions = session.query(Transaction).all()

    return transactions
    
# Create a Transaction
@router_v1.post("/transaction", response_model=TransactionSchema)
def create_transaction(transaction: TransactionCreate,
                       api_key: str = Depends(get_api_key),
                       session: Session = Depends(get_session)):
    db_transaction = Transaction(**transaction.dict())
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

# Get a Transaction
@router_v1.get("/transaction/{transaction_id}", response_model=TransactionSchema)
def read_transaction(transaction_id: int,
                     api_key: str = Depends(get_api_key),
                     session: Session = Depends(get_session)):
    transaction = (session.query(Transaction).
                   filter(Transaction.transaction_id == transaction_id).first())
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
#     return transaction

# Update a Transaction
@router_v1.put("/transaction/{transaction_id}",
               response_model=TransactionSchema)
def update_transaction(transaction_id: int,
                       transaction: TransactionCreate,
                       api_key: str = Depends(get_api_key),
                       session: Session = Depends(get_session)):
    db_transaction = (session.query(Transaction)
                      .filter(Transaction.transaction_id == transaction_id).first())
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for var, value in transaction:
        setattr(db_transaction, var, value)
    session.commit()
    return db_transaction

# Delete a Transaction
@router_v1.delete("/transaction/{transaction_id}",
                  status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int,
                       api_key: str = Depends(get_api_key),
                       session: Session = Depends(get_session)):
    transaction = (session.query(Transaction)
                   .filter(Transaction.transaction_id == transaction_id).first())
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return None

# Get all Products
@router_v1.get("/products", response_model=List[ProductSchema])
def read_product_list( api_key: str = Depends(get_api_key),
                       session: Session = Depends(get_session)):
    product_list = session.query(Product).all()
    return product_list



# Create a Product
@router_v1.post("/product", response_model=ProductSchema,
                status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate,
                   api_key: str = Depends(get_api_key),
                   session: Session = Depends(get_session)):
    product_db = Product(**product.dict())
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    return product_db

# Get a Product
@router_v1.get("/product/{id}", response_model=ProductSchema)
def read_product(id: int,
                 api_key: str = Depends(get_api_key),
                 session: Session = Depends(get_session)):
    product = session.query(Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    return product

# Update a Product
@router_v1.put("/product/{id}", response_model=ProductSchema)
def update_product(id: int, product: ProductCreate,
                   api_key: str = Depends(get_api_key),
                   session: Session = Depends(get_session)):
    product_db = session.query(Product).get(id)
    if not product_db:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    for var, value in product.dict().items():
        setattr(product_db, var, value)
    session.commit()
    return product_db

# Delete a Product
@router_v1.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int,
                   api_key: str = Depends(get_api_key),
                   session: Session = Depends(get_session)):
    product = session.query(Product).get(id)
    if product:
        session.delete(product)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Product with id {id} not found")
    return None



# ... (include the remaining route-related content here)
