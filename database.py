import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# FIXED: use DATABASE_URL from environment variable instead of hardcoding
db_url = os.getenv("DATABASE_URL", "postgresql://postgres:shivesh%402006@localhost:5432/shivesh")
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
