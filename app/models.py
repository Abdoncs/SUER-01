from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class EnergyRecord(Base):
    __tablename__ = "energy_records"

    id = Column(Integer, primary_key=True)
    usuario = Column(String, nullable=False)
    geracao_kwh = Column(Float, nullable=False)
    consumo_kwh = Column(Float, nullable=False)
    saldo_kwh = Column(Float, nullable=False)
    valor_bruto = Column(Float, nullable=False)
    taxa_distribuidora = Column(Float, nullable=False)
    taxa_suer = Column(Float, nullable=False)
    valor_liquido = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)