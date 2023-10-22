from pydantic import BaseModel

# Create User Schema (Pydantic Model)
class UserCreate(BaseModel):
    name: str
    age: int
    gender: str
    location: str
    preferences: str

    class Config:
        orm_mode = True
        
# Complete User Schema (Pydantic Model)
class UserSchema(BaseModel):
    user_id: int
    name: str
    age: int
    gender: str
    location: str
    preferences: str

    class Config:
        orm_mode = True
