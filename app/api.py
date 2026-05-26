from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import EnergyRecord
from app.liquidation import calcular_liquidacao

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, init_db
from app.models import EnergyRecord
from app.liquidation import calcular_liquidacao

# Cria a tabela se não existir
init_db()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SUER Energy API")

class EnergiaPayload(BaseModel):
    usuario: str
    geracao_kwh: float
    consumo_kwh: float
    timestamp: datetime = None

@app.get("/")
def root():
    return {"status": "SUER Simulator Online"}

@app.post("/energia")
def receber_energia(payload: EnergiaPayload):
    saldo = payload.geracao_kwh - payload.consumo_kwh
    financeiro = calcular_liquidacao(saldo)
    db: Session = SessionLocal()
    registro = EnergyRecord(
        usuario=payload.usuario,
        geracao_kwh=payload.geracao_kwh,
        consumo_kwh=payload.consumo_kwh,
        saldo_kwh=saldo,
        valor_bruto=financeiro["valor_bruto"],
        taxa_distribuidora=financeiro["taxa_distribuidora"],
        taxa_suer=financeiro["taxa_suer"],
        valor_liquido=financeiro["valor_liquido"]
    )
    db.add(registro)
    db.commit()
    db.close()
    return {"message": "Registrado", "saldo_kwh": saldo, **financeiro}

@app.get("/registros")
def listar_registros():
    db: Session = SessionLocal()
    registros = db.query(EnergyRecord).all()
    resultado = []
    for r in registros:
        resultado.append({
            "usuario": r.usuario,
            "saldo_kwh": r.saldo_kwh,
            "valor_liquido": r.valor_liquido,
            "timestamp": r.timestamp
        })
    db.close()
    return resultado