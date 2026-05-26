import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os

# Importa a função de inicialização do banco (cria a tabela se necessário)
from app.database import init_db

# Inicializa o banco (cria a tabela se não existir)
init_db()

# Obtém a URL do banco (mesma lógica do database.py)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///suer.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

st.set_page_config(page_title="SUER Dashboard", layout="wide")
st.title("📊 Dashboard Acadêmico SUER")

# Consulta os dados
try:
    query = "SELECT * FROM energy_records ORDER BY timestamp DESC"
    df = pd.read_sql(query, engine)

    if df.empty:
        st.warning("⚠️ Nenhum dado ainda. Execute o simulador (http_simulator.py) e aguarde o envio de dados.")
    else:
        st.subheader("📋 Últimos Registros")
        st.dataframe(df.head(50), use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔋 Geração Total (kWh)", f"{df['geracao_kwh'].sum():.2f}")
        with col2:
            st.metric("💰 Valor Líquido Total (R$)", f"R$ {df['valor_liquido'].sum():.2f}")
        with col3:
            st.metric("⚖️ Saldo Médio (kWh)", f"{df['saldo_kwh'].mean():.2f}")

        st.subheader("📊 Saldo Médio por Usuário")
        saldo_por_usuario = df.groupby("usuario")["saldo_kwh"].mean().sort_values(ascending=False)
        st.bar_chart(saldo_por_usuario)

        st.subheader("📈 Evolução Temporal (últimos 100 registros)")
        if len(df) > 1:
            df_evol = df.head(100).copy()
            df_evol["timestamp"] = pd.to_datetime(df_evol["timestamp"])
            df_evol = df_evol.sort_values("timestamp")
            st.line_chart(df_evol.set_index("timestamp")[["geracao_kwh", "consumo_kwh"]])
except Exception as e:
    st.error(f"Erro ao carregar dados do banco: {e}")
    st.info("Verifique se o banco de dados está acessível e se a tabela 'energy_records' foi criada.")