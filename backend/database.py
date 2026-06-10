import os
import certifi  # <-- Importa o pacote de certificados instalado
from dotenv import load_dotenv
from pymongo import MongoClient

def conectar_banco():
    load_dotenv()
    url_conexao = os.getenv("URL_BANCO")
    
    try:
        # Passamos o tlsCAFile para o Mongo usar os certificados seguros do certifi
        cliente = MongoClient(url_conexao, tlsCAFile=certifi.where())
        db = cliente.get_database("clinica_pet")
        
        cliente.admin.command('ping')
        print("Conexão com o MongoDB estabelecida com sucesso!")
        return db
        
    except Exception as erro:
        print(f"Erro ao conectar com o banco: {erro}")
        return None