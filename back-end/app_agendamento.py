from flask import Flask, request
from agendamento import agendar_consulta

app = Flask(__name__)

#Teste para ver se o servidor funciona
@app.route('/')
def home():
    return "Servidor da Clínica Pet funcionando!"

#Rota que recebe os dados do HTML
@app.route('/agendar_pelo_site', methods=['POST'])
def receber_agendamento_do_site():

    e_tutor = request.form.get("email_tutor")
    if e_tutor:
        e_tutor = e_tutor.strip()

    i_pet = request.form.get("id_pet")
    if i_pet:
        i_pet = i_pet.strip()

    servico = request.form.get("servico")
    data_c = request.form.get("data")
    hora_c = request.form.get("hora")
    obs = request.form.get("observacoes")

    print("\n--- RAIO-X DO FLASK ---")
    print(f"Email recebido: '{e_tutor}'")
    print(f"ID do Pet recebido: '{i_pet}'")
    print("-----------------------\n")

    motivo_completo = f"{servico} - {obs}"
    resposta_do_banco = agendar_consulta(e_tutor, i_pet, data_c, hora_c, motivo_completo)
    return(resposta_do_banco)

if __name__ == '__main__':
    app.run(debug=True)