from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:shivesh%402006@localhost:5432/shivesh"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
