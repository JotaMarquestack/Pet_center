from database import conectar_banco
import uuid

def agendar_consulta(email_tutor, id_pet, data_consulta, hora_consulta, motivo):
    db = conectar_banco()
    if db is None:
        return "Erro de conexão com o banco."
    
    col_clientes = db.get_collection("clientes")
    col_agendamentos = db.get_collection("agendamentos")

    print("\n--- INVESTIGAÇÃO MONGODB ---")
    print(f"Buscando Email: '{email_tutor}' | Pet: '{id_pet}'")
    
    tutor_so_email = col_clientes.find_one({"email": email_tutor})
    if tutor_so_email:
        print("Passo A: Tutor encontrado pelo e-mail!")
        print(f"Lista de pets no banco: {tutor_so_email.get('pets', [])}")
    else:
        print("Passo A FALHOU: O banco diz que esse e-mail não existe na collection 'clientes'.")

    vinculo_valido = col_clientes.find_one({
        "email": email_tutor,
        "pets.id_pet": id_pet
    })

    if vinculo_valido:
        print("Passo B: Vínculo Pet+Tutor validado!")
    else:
        print("Passo B FALHOU: O banco não conseguiu cruzar o e-mail com o ID do Pet.")
    print("----------------------------\n")

    if not vinculo_valido:
        return "Erro de Validação: Tutor não encontrado ou o Pet informado não pertence a este tutor."
    
    id_consulta = f"CONS-{uuid.uuid4().hex[:6].upper()}"

    novo_agendamento = {
        "id_consulta": id_consulta,
        "email_tutor": email_tutor,
        "id_pet": id_pet,
        "data": data_consulta,
        "hora": hora_consulta,
        "motivo": motivo,
        "status": "Agendado"
    }

    col_agendamentos.insert_one(novo_agendamento)
    return f"Sucesso! Consulta {id_consulta} agendada para o dia {data_consulta} às {hora_consulta}."

