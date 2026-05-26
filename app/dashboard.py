import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///suer.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

st.title("Dashboard Acadêmico SUER")

query = "SELECT * FROM energy_records"
df = pd.read_sql(query, engine)

if df.empty:
    st.warning("Sem dados ainda. Execute o simulador HTTP.")
else:
    st.subheader("Registros")
    st.dataframe(df)
    st.subheader("Energia Total Gerada")
    st.metric(label="kWh Total", value=round(df["geracao_kwh"].sum(), 2))
    st.subheader("Liquidação Financeira")
    st.metric(label="Valor Líquido Total", value=f"R$ {round(df['valor_liquido'].sum(), 2)}")
    st.subheader("Saldo Médio por Usuário")
    st.bar_chart(df.groupby("usuario")["saldo_kwh"].mean())