from pydantic import BaseModel

class TransactionCreate(BaseModel):
    user_id: int
    product_id: int
    
    class Config:
        orm_mode = True

class TransactionSchema(BaseModel):
    transaction_id: int
    user_id: int
    product_id: int

    class Config:
        orm_mode = True
