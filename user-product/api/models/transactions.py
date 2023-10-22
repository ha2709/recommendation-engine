from sqlalchemy import Column, Integer
from db.database import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
