import os
import dns.resolver  
from dotenv import load_dotenv
from pymongo import MongoClient

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

load_dotenv()
url_conexao = os.getenv("URL_BANCO")

try:
    print("Tentando conectar ao banco de dados...")
    cliente = MongoClient(url_conexao)
    
    db = cliente["clinica_pet"]
    
    cliente.admin.command('ping')
    print("Sucesso! Conexão estabelecida com o MongoDB Atlas.")
    
except Exception as erro:
    print("Erro ao conectar:")
    print(erro)