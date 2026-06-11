from database import conectar_banco
import uuid
from bson import ObjectId  # Necessário para ler o ID do MongoDB

def agendar_consulta(email_tutor, id_pet, data_consulta, hora_consulta, motivo):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."
    
    col_pets = db.get_collection("pets")
    col_agendamentos = db.get_collection("agendamentos")

    print("\n--- INVESTIGAÇÃO MONGODB (AGENDAMENTO) ---")
    print(f"Buscando Email do Tutor: '{email_tutor}' | ID do Pet: '{id_pet}'")
    
    # Como o HTML enviou o ID gerado pelo Mongo, precisamos convertê-lo para ObjectId
    try:
        id_pet_objeto = ObjectId(id_pet)
    except Exception:
        # Caso o ID não venha no formato padrão do Mongo (ex: vindo de testes antigos)
        id_pet_objeto = id_pet

    # Passo Único e Seguro: O pet existe e pertence a esse tutor?
    pet_valido = col_pets.find_one({
        "_id": id_pet_objeto,
        "email_tutor": email_tutor
    })

    if pet_valido:
        print(f"Sucesso: O pet '{pet_valido.get('nome_pet')}' foi encontrado e pertence a {email_tutor}!")
    else:
        print("FALHA: Nenhum pet com esse ID pertence a este e-mail na collection 'pets'.")
    print("------------------------------------------\n")

    if not pet_valido:
        return "Erro de Validação: O pet informado não foi encontrado ou não pertence a este tutor."
    
    # Gera um identificador único amigável para a consulta
    id_consulta = f"CONS-{uuid.uuid4().hex[:6].upper()}"

    novo_agendamento = {
        "id_consulta": id_consulta,
        "email_tutor": email_tutor,
        "id_pet": id_pet, # Mantemos salvo como string para facilitar futuras buscas
        "nome_pet": pet_valido.get("nome_pet"), # Prática NoSQL: salvar o nome direto ajuda na performance
        "data": data_consulta,
        "hora": hora_consulta,
        "motivo": motivo,
        "status": "Agendado"
    }

    col_agendamentos.insert_one(novo_agendamento)
    return f"Sucesso! Consulta {id_consulta} agendada para o dia {data_consulta} às {hora_consulta}."