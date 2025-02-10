import os
from pymongo import MongoClient
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))

load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não foi definida.")

client = MongoClient(DATABASE_URL)

db_name = os.getenv("DB_NAME", "trabalho_3")  # Ex.: defina DB_NAME no .env ou use "meu_banco" como padrão
db = client[db_name]

def get_db():
    return db
