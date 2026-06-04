from database import conectar_banco

# Conexão com o MongoDB


db = conectar_banco()
col = db.get_collection("clientes")

# Cadastro Básico e inserção de dados do Tutor e Pet no MongoDB
if db is not None:
    print("\n--- INICIANDO NOVO CADASTRO ---")
    tutor_nome = input("Nome do tutor: ")
    tutor_cpf = input("CPF do tutor: ")
    tutor_telefone = input("Telefone do tutor: ")
    tutor_email = input("Email do tutor: ")

    pet_nome = input("Nome do Pet: ")
    pet_especie = input("Espécie do Pet: ")
    pet_raca = input("Raça do Pet: ")
    pet_sexo = input("Sexo do Pet (M/F): ")
    pet_peso = float(input("Peso do Pet (em kg, use ponto, ex: 5.3): "))

    pet_castrado_resposta = input("Seu pet já é castrado? (S/N): ").strip().upper()
    pet_castrado = True if pet_castrado_resposta == 'S' else False

    pet_observacao = input("Seu pet possui alguma alergia ou observação?: ")

    dados = {
        "tutor": {
            "nome": tutor_nome,
            "cpf": tutor_cpf,
            "telefone": tutor_telefone,
            "email": tutor_email
        },
        "pet": {
            "nome": pet_nome,
            "especie": pet_especie,
            "raca": pet_raca,
            "sexo": pet_sexo,
            "peso_kg": pet_peso,
            "castrado": pet_castrado,
            "observacoes": pet_observacao
        }
    }
    print("\n Estrutura montada com sucesso!")

col.insert_one(dados)