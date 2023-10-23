from pydantic import BaseModel

# Create Product Schema (Pydantic Model)
class ProductCreate(BaseModel):
    category: str
    Product_name: str
    description: str
    tags: str
    class Config:
        orm_mode = True
        
# Complete Product Schema (Pydantic Model)
class ProductSchema(BaseModel):
    product_id: int
    category: str
    Product_name: str
    description: str
    tags: str

    class Config:
        orm_mode = True
