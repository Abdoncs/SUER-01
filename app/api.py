from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.models import EnergyRecord
from app.liquidation import calcular_liquidacao

# Garante que a tabela exista antes de iniciar a API
init_db()

app = FastAPI(title="SUER Energy API")

class EnergiaPayload(BaseModel):
    usuario: str
    geracao_kwh: float
    consumo_kwh: float
    timestamp: Optional[datetime] = None

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
    db.refresh(registro)
    db.close()

    return {
        "message": "Registrado com sucesso",
        "saldo_kwh": saldo,
        **financeiro
    }

@app.get("/registros")
def listar_registros():
    db: Session = SessionLocal()
    registros = db.query(EnergyRecord).all()
    resultado = []
    for r in registros:
        resultado.append({
            "usuario": r.usuario,
            "geracao_kwh": r.geracao_kwh,
            "consumo_kwh": r.consumo_kwh,
            "saldo_kwh": r.saldo_kwh,
            "valor_liquido": r.valor_liquido,
            "timestamp": r.timestamp.isoformat() if r.timestamp else None
        })
    db.close()
    return resultado