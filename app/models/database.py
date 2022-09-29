from app.utils.config import load_config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = load_config()
SQLALCHEMY_DATABASE_URL = f"postgresql://{config.db.db_user}:{config.db.db_pass}@{config.db.db_host}/{config.db.db_database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
