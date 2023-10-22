from sqlalchemy import Column, Integer, String
from db.database import Base

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    category = Column(String(50))
    Product_name = Column(String(100))
    description = Column(String(200))
    tags = Column(String(200))
