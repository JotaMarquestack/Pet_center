import bcrypt #Criptografia da senha
import uuid #Geração de ID 
from database import conectar_banco #Conexão com o database.py

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
        "telefone": telefone_limpo,
        "email": email,
        "senha": senha_criptografada, 
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

    #Barreira de validação do pet
    erros_pet = []

    #Validação do sexo
    sexo_limpo = str(sexo).strip().upper()
    if sexo_limpo not in ["M", "F"]:
        erros_pet.append("O sexo do pet deve ser exclusivamente 'M' ou 'F'.")
    
    #Validação do castrado
    if not isinstance(castrado, bool):
        erros_pet.append("O status de castração deve ser um valor verdadeiro ou falso")

    #Validação do usuário    
    if not tutor:
        return f"Erro, tutor não encontrado. Não é possível cadastrar o pet"
    
    #Validação do peso
    try:
        peso_texto = str(peso).replace(",",".")
        peso_seguro = float(peso_texto)
    except(ValueError):
        erros_pet.append("Erro de validação: O peso deve ser um número válido (Ex: 5.5 ou 5,5).")
    
    if len(erros_pet)>0:
        mensagem_final = "O cadastro do pet falhou pelos seguintes motivos:\n- " + "\n- ".join(erros_pet)
        return mensagem_final
    
    #Gerador de ID único para o pet:
    id_unico_pet = f"PET-{uuid.uuid4().hex[:6].upper()}"

    novo_pet = {
        "id_pet": id_unico_pet,
        "nome": nome_pet,
        "especie": especie,
        "raca": raca,
        "peso": peso_seguro,
        "castrado": castrado,
        "sexo": sexo_limpo,
        "observacoes": observacoes
    }

    col.update_one(
        {"email":email_tutor},
        {"$push": {"pets": novo_pet}}
    )

    return f"Sucesso! O pet {nome_pet} (ID: {id_unico_pet}) foi adicionado à ficha de {tutor['nome']}"

def visualizar_tutor(email):
    db = conectar_banco()
    if db is None:
        return f"Erro de conexão com o banco."
    
    col = db.get_collection("clientes")
    tutor = col.find_one({"email": email})

    if not tutor:
        return f"Erro: tutor não encontrado no sistema."
    
    #Ficha do cliente
    ficha = f"\n========================================="
    ficha += f"\n   FICHA DO CLIENTE: {tutor['nome'].upper()}"
    ficha += f"\n========================================="
    ficha += f"\nCPF: {tutor['cpf']}"
    ficha += f"\nTelefone: {tutor['telefone']}"
    ficha += f"\nE-mail: {tutor['email']}"
    ficha += f"\n-----------------------------------------"
    ficha += f"\nPETS CADASTRADOS:"

    #Lista se o tutor não ter pets
    if not tutor.get("pets") or len(tutor["pets"]) == 0:
        ficha += "\n[ Nenhum pet cadastrado para este tutor.]"

    else:
        for pet in tutor["pets"]:
            ficha += f"\n\n🐾 ID: {pet['id_pet']}"
            ficha += f"\n   Nome: {pet['nome']} | Espécie: {pet['especie']} ({pet['raca']})"
            ficha += f"\n   Peso: {pet['peso']} Kg | Castrado: {'Sim' if pet['castrado'] else 'Não'} | Sexo: {pet['sexo']}"
            if pet['observacoes']:
                ficha += f"\n Obs. Médicas: {pet['observacoes']}"
    
    ficha += f"\n========================================="
    return ficha

def atualizar_pet(id_pet, novo_peso, novo_castrado, novas_observacoes):
    db = conectar_banco()
    if db is None:
        return f"Erro de conexão com o banco."
    
    col = db.get_collection("clientes")

    tutor = col.find_one({"pets.id_pet": id_pet})
    if not tutor:
        return f"Erro: Nenhum pet com o ID {id_pet} foi encontrado no sistema."
    
    try:
        peso_texto = str(novo_peso).replace(",", ".")
        peso_seguro = float(peso_texto)
    except ValueError:
        return "Erro de Validação: O peso deve ser um número válido (ex: 12.5)."
    
    if not isinstance(novo_castrado, bool):
        return "Erro de Validação: O status de castração deve ser Verdadeiro ou Falso."
    
    col.update_one(
        {"pets.id_pet": id_pet},
        {
            "$set": {
                "pets.$.peso": peso_seguro,
                "pets.$.castrado": novo_castrado,
                "pets.$.observacoes": novas_observacoes
            }
        }
    )

    return f"Sucesso! Os dados do pet {id_pet} foram atualizados no prontuário."

def redefinir_senha_tutor(email, nova_senha):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."
    
    col = db.get_collection("clientes")
    tutor = col.find_one({"email": email})
    if not tutor:
        return "Erro: Tutor não encontrado no sistema."

    if len(nova_senha) < 8 or not any(letra.isupper() for letra in nova_senha) or not any(letra.isdigit() for letra in nova_senha):
        return "Erro: A nova senha deve ter no mínimo 8 caracteres, contendo pelo menos uma letra maiúscula e um número."
    
    senha_bytes = nova_senha.encode('utf-8')
    nova_senha_criptografada = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())


    col.update_one(
        {"email": email},
        {
            "$set": {
                "senha":  nova_senha_criptografada,
            }
        }
    )
    return f"Sucesso! A senha para o e-mail {email} foi atualizada com segurança."

def atualizar_perfil_tutor(email, novo_telefone, novo_nome):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."
    
    col = db.get_collection("clientes")
    tutor = col.find_one({"email": email})

    if not tutor:  
        return "Erro: Tutor não encontrado no sistema."
      
    erros = []

    novo_telefone_limpo = novo_telefone.replace(" ", "").replace("-","").replace("(","").replace(")","")
    if not novo_telefone_limpo.isdigit() or len(novo_telefone_limpo) not in [10, 11]:
        erros.append("O telefone deve conter 10 ou 11 números (incluindo o DDD).")
    
    if any(letra.isdigit() for letra in novo_nome):
        erros.append("O nome não pode conter números.")
    
    if len(erros) > 0:
        mensagem_final = "A atualização falhou:\n- " + "\n- ".join(erros)
        return mensagem_final
    
    col.update_one(
        {"email": email},
        {
            "$set": {
                "telefone": novo_telefone_limpo,
                "nome": novo_nome
            }
        }
    )
    return f"Sucesso! O nome e o telefone de {tutor['nome']} foi atualizada com segurança."

def remover_pet(id_pet):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."

    col = db.get_collection("clientes")
    tutor = col.find_one({"pets": id_pet})
    if not tutor:
        return f"Erro: Nenhum pet com o ID {id_pet} foi encontrado."

    col.update_one(
        {"pets.id_pet": id_pet},
        {
            "$pull": {
                "pets": {"id_pet": id_pet}
            }
        }
    )
    return f"Sucesso! O pet com ID {id_pet} foi removido do prontuário."

def deletar_tutor_completo(email):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."

    col = db.get_collection("clientes")
    tutor = col.find_one({"email":email})
    if not tutor:
        return f"Erro: Tutor não encontrado no sistema"
    
    col.delete_one({"email": email})
    
    return f"Aviso: O tutor {tutor['nome']} e todos os seus pets foram apagados para sempre."
