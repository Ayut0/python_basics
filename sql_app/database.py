from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQlite
SQL_ALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# PostgreSQL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Create a SQLAlchemy engine
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal class, it's not a database session yet
# Once we create an instance of it, this instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
