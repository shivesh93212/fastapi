from fastapi import Depends, FastAPI
from models import ProductSchema
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"message": "Welcome to Shivesh's website"}


# Sample product list
products = [
    ProductSchema(id=1, name="laptop", price=50000),
    ProductSchema(id=2, name="shivesh", price=5000),
    ProductSchema(id=3, name="phone", price=20000),
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count = db.query(database_models.Product).count()  # fixed: call count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))  # Assuming Pydantic v2
        db.commit()


init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


@app.get("/product/{id}")
def get_product_by_id(id: int,db: Session = Depends(get_db)):
    # You are still using in-memory list here (as per your code)
    db_product= db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
            return db_product
    return {"error": "product not found"}


@app.post("/product")
def add_product(product: Product,db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if db_product:
        db_product.name = product.name  # type: ignore
        db_product.price = product.price  # type: ignore
        db.commit()
        db.refresh(db_product)  # optional but useful
        return {"message": "product updated", "product": db_product}
    else:
        return {"error": "no product found"}


@app.delete("/product")
def delete_product(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
           db.delete(db_product) 
           db.commit()
           return {"message": "product deleted"}     
    else:
        return {"error": "product not found"}

# python -m uvicorn fast:app --reload --port 9000

# how to save data in database
# uvicorn fast:app --reload --port 9000







           




     
     
