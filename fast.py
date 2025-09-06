from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from models import ProductSchema   # ✅ Pydantic schema
from database import SessionLocal, engine, Base
import database_models             # ✅ SQLAlchemy models

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return {"message": "Welcome to Shivesh's website"}


# Sample product list (used only to seed DB)
products = [
    ProductSchema(id=1, name="laptop", price=50000),
    ProductSchema(id=2, name="shivesh", price=5000),
    ProductSchema(id=3, name="phone", price=20000),
]


# ✅ Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ FIX: use SessionLocal, not "session"
def init_db():
    db = SessionLocal()
    try:
        count = db.query(database_models.Product).count()
        if count == 0:
            for product in products:
                db.add(database_models.Product(**product.model_dump()))  # Pydantic v2
            db.commit()
    finally:
        db.close()


# Run DB initializer
init_db()


# ✅ FIX: use database_models.Product instead of Product (not imported)
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return {"error": "product not found"}


# ✅ FIX: type hint to ProductSchema, and map correctly
@app.post("/product")
def add_product(product: ProductSchema, db: Session = Depends(get_db)):
    new_product = database_models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put("/product/{id}")
def update_product(id: int, product: ProductSchema, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db.commit()
        db.refresh(db_product)
        return {"message": "product updated", "product": db_product}
    else:
        return {"error": "no product found"}


@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "product deleted"}
    else:
        return {"error": "product not found"}


# Run locally:
# uvicorn fast:app --reload --port 9000
