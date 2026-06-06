import bcrypt
from database import conectar_banco

def cadastrar_tutor(cpf, nome, telefone, email, senha):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."
    
    col = db.get_collection("clientes")

    #Lista para erros
    erros = []

    #Definição para o CPF barrado
    cpf_limpo = cpf.replace(".", "").replace("-", "").strip()
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        erros.append("O CPF deve conter exatamente 11 números")
    
    #Definição para o e-mail barrado:
    if "@" not in email or "." not in email:
        erros.append("Erro de validação: Formato de e-mail inválido.")

    #Definição para o nome incorreto:
    if any(letra.isdigit() for letra in nome):
        erros.append("O nome não pode conter números.")
    
    #Definição para o número do celular:
    telefone_limpo = telefone.replace(" ", "").replace("-","").replace("(","").replace(")","")
    if not telefone_limpo.isdigit() or len(telefone_limpo) not in [10, 11]:
        erros.append("O telefone deve conter 10 ou 11 números (incluindo o DDD).")

    #Definição para a senha mínima:
    if len(senha) < 8 or not any(letra.isupper() for letra in senha) or not any(letra.isdigit for letra in senha):
        erros.append("A senha deve ter no mínimo 8 caracteres, contendo pelo menos uma letra maiúscula e um número.")
    
    if len(erros) > 0:
        mensagem_final = "O cadastro falhou pelos seguintes motivos:\n " + " \n ".join(erros)
        return(mensagem_final)
    
    #Pesquisa para verificar se o Email ou o CPF já estão cadastrados no sistema.
    if col.find_one({"email": email}):
        return f"Erro: O email {email} já está cadastrado!"
    if col.find_one({"cpf": cpf_limpo}):
        return f"Erro: O cpf {cpf_limpo} já consta no sistema!"
    
    #Geração da senha criptografada
    senha_bytes = senha.encode('utf-8')
    senha_criptografada = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    
    novo_cliente = {
        "nome": nome,
        "cpf": cpf_limpo,
        "telefone": telefone,
        "email": email,
        "senha": senha_criptografada, #Tem que deixar esse invisível
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

    #Checagem se o email foi encontrado:
    if cliente:
        #Transformar senha em bytes
        senha_digitada_bytes = senha_digitada.encode('utf-8')

        #Bycrypt pega a senha em bytes e compara com a senha no banco de dados
        if bcrypt.checkpw(senha_digitada_bytes, cliente["senha"]):
            return f"Login aprovado! Acesso liberado para {cliente['nome']}"
        else:
            return f"Erro: Email ou senha incorretos."
    else:
        return f"Erro: Email ou senha incorretos."

def cadastrar_pet(email_tutor, nome_pet, especie, raca, peso, castrado, sexo, observacoes):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."
    
    col = db.get_collection("clientes")
    tutor = col.find_one({"email":email_tutor})

    if not tutor:
        return f"Erro, tutor não encontrado. Não é possível cadastrar o pet"
    
    try:
        peso_texto = str(peso).replace(",",".")
        peso_seguro = float(peso_texto)
    except:
        return f"Erro de validação: O peso deve ser um número válido (Ex: 5.5 ou 5,5)."

    novo_pet = {
        "nome": nome_pet,
        "especie": especie,
        "raca": raca,
        "peso": float(peso),
        "castrado": castrado,
        "sexo": sexo,
        "observacoes": observacoes
    }

    col.update_one(
        {"email":email_tutor},
        {"$push": {"pets": novo_pet}}
    )

    return f"Sucesso! O pet {nome_pet} foi adicionado à ficha de {tutor['nome']}"