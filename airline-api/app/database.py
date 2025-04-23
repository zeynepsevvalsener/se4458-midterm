# app/database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) .env içindeki DATABASE_URL'i yüklüyoruz
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# 2) engine tanımı (MUST come before SessionLocal)
engine = create_engine(DATABASE_URL, echo=True)

# 3) Her istek için DB session'ı sağlayan factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4) Tüm modellerin extend edeceği Base sınıfı
Base = declarative_base()

def init_db():
    """Uygulama başlarken tabloların oluşturulması için çağrılır."""
    Base.metadata.create_all(bind=engine)
