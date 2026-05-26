from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class EnergyRecord(Base):
    __tablename__ = "energy_records"
    id = Column(Integer, primary_key=True)
    usuario = Column(String)
    geracao_kwh = Column(Float)
    consumo_kwh = Column(Float)
    saldo_kwh = Column(Float)
    valor_bruto = Column(Float)
    taxa_distribuidora = Column(Float)
    taxa_suer = Column(Float)
    valor_liquido = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)