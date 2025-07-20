import os
import psycopg2 as pg
from sqlalchemy import create_engine
from dotenv import load_dotenv
import panel as pn

# Carrega as variáveis do arquivo .env
load_dotenv()

# Lê as variáveis de ambiente
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

try:
    # Cria conexão com psycopg2 para operações de escrita (INSERT, UPDATE, DELETE)
    con = pg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

    # Define a string de conexão para o SQLAlchemy para leitura (SELECT)
    db_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    engine = create_engine(db_url)

except Exception as e:
    pn.state.notifications.error(f'Erro ao conectar ao banco de dados: {e}')
    con = None
    engine = None