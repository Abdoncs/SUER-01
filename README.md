# SUER Simulator – Deploy no Render

## Execução local (desenvolvimento)
1. Clone o repositório.
2. Crie um ambiente virtual e instale dependências: `pip install -r requirements.txt`
3. Execute a API: `uvicorn app.api:app --reload`
4. Em outro terminal, execute o dashboard: `streamlit run app/dashboard.py`
5. Em um terceiro terminal, execute o simulador: `python simulator/http_simulator.py`
   - Certifique-se que `API_URL` no simulador aponte para `http://localhost:8000/energia`

## Deploy no Render (gratuito)
1. Crie um repositório no GitHub com todos os arquivos acima.
2. Acesse [render.com](https://render.com), faça login e clique em **New +** → **Blueprint**.
3. Conecte seu repositório.
4. O Render lerá o `render.yaml` e criará automaticamente:
   - Banco PostgreSQL
   - API FastAPI
   - Dashboard Streamlit
5. Após o deploy (cerca de 5 minutos), obtenha as URLs:
   - API: `https://suer-api.onrender.com`
   - Dashboard: `https://suer-dashboard.onrender.com`
6. Edite o `simulator/http_simulator.py` localmente, alterando `API_URL` para a URL da sua API.
7. Execute o simulador: `python simulator/http_simulator.py`
8. Acesse o dashboard e visualize os dados em tempo real.

> O banco de dados é compartilhado entre a API e o dashboard automaticamente via variável de ambiente `DATABASE_URL`.