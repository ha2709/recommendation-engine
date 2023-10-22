from sqlalchemy import Column, Integer, String
from db.database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(10))
    location = Column(String(50))
    preferences = Column(String(100))
