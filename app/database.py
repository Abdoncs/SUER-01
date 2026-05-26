import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Obtém a URL do banco (Render fornece DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///suer.db")

# Correção para PostgreSQL no Render
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuração específica para SQLite
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Cria todas as tabelas definidas nos modelos, se não existirem."""
    # Importamos os modelos aqui para registrar as tabelas no Base.metadata
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado (tabelas verificadas/criadas).")