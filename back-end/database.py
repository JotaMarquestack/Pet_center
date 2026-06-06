#Arquivo para o teste de conexão com o MongoDB
import os
import dns.resolver  
from dotenv import load_dotenv
from pymongo import MongoClient

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

def conectar_banco():
    load_dotenv()
    url_conexao = os.getenv("URL_BANCO")

    try:
        cliente = MongoClient(url_conexao)
        db = cliente.get_database("clinica_pet")

        cliente.admin.command('ping')
        return db
    
    except Exception as erro:
        print(f"Erro ao conectar com o banco: {erro}")
        return None