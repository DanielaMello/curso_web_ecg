from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Pega a URL do banco das variáveis de ambiente
DATABASE_URL: str = os.environ["DATABASE_URL"]

engine=create_engine(DATABASE_URL)
Session=sessionmaker(bind=engine)

# Classe base para os modelos ORM
class Base(DeclarativeBase):
    pass

# O motor que gerencia as conexões
engine = create_engine(DATABASE_URL, echo=True)

# Uma fábrica para criar novas sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()