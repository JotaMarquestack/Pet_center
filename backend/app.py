from flask import Flask, render_template, request, redirect, url_for, flash, session
from login_cadastro import cadastrar_tutor, login_tutor
from agendamento import agendar_consulta
import os 
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../frontend',
            static_url_path='')

app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=30)

#Rota de cadastro e login
@app.route('/processar_login', methods=['POST'])
def processar_login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    lembrar = request.form.get('lembrar')
    
    resultado = login_tutor(email, senha)
    
    if resultado:
        session['usuario_logado'] = email
        
        if lembrar == 'on':
            session.permanent = True
        else:
            session.permanent = False
            
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for('home')) 
        
    else:
        flash("E-mail ou senha incorretos.", "danger")
        return redirect(url_for('login_page'))



@app.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    dados = request.form.to_dict()
    print(f"DADOS RECEBIDOS PELO FLASK: {dados}") 

    nome = dados.get('nome')
    email = dados.get('email')
    cpf = dados.get('cpf')
    telefone = dados.get('telefone')
    senha = dados.get('senha')

    resultado = cadastrar_tutor(cpf, nome, telefone, email, senha)
    
    if resultado:
        flash("Cadastro realizado com sucesso! Faça seu login.","sucess")
        return redirect(url_for('login_page'))
    else:
        flash("Erro no cadastro! Verifique seus dados ou se o CPF/E-mail já existem.","danger")
        return redirect(url_for('cadastro_page'))



@app.route('/')
def index():
    if 'usuario_logado' not in session:
        flash("Acesso negado! Por favor, faça login primeiro.", "warning")
        return redirect(url_for('login_page'))
    
    email_logado = session.get('usuario_logado')
    return render_template('home.html', usuario=email_logado)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastro.html')

@app.route('/home')
def home():
    return render_template('home.html')


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

    motivo_completo = f"{servico} - {obs}"
    
    resposta_do_banco = agendar_consulta(e_tutor, i_pet, data_c, hora_c, motivo_completo)
    return(resposta_do_banco)

if __name__ == '__main__':
    app.run(debug=True)

