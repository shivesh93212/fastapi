from pydantic import BaseModel

# FIXED: renamed Product -> ProductSchema to avoid conflict with SQLAlchemy model
class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
