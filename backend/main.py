from database import conectar_banco

def cadastrar_tutor(cpf, nome, telefone, email, senha):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."
    
    col = db.get_collection("clientes")

    if col.find_one({"email": email}):
        return f"Erro: O email {email} já está cadastrado!"
    if col.find_one({"cpf": cpf}):
        return f"Erro: O cpf {cpf} já consta no sistema!"
    
    novo_cliente = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "email": email,
        "senha": senha, #Tem que deixar esse invisível
        "pets": []
    }
    col.insert_one(novo_cliente)
    return f"Sucesso! Sua conta foi criada para {email}."
    
def login_tutor(email, senha_digitada):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."
    
    col = db.get_collection("clientes")
    cliente = col.find_one({"email": email})

    if cliente and cliente["senha"] == senha_digitada:
        return f"Login aprovado! Acesso liberado para {cliente['nome']}."
    else:   
        return f"Erro: Email ou senha incorretos."