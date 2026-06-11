import os 
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Importação das funções do teu grupo
from agendamento import agendar_consulta
from login_cadastro import cadastrar_tutor, login_tutor

load_dotenv()

app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../frontend',
            static_url_path='')

app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=30)


# ==========================================
# VERIFICAÇÃO DE SEGURANÇA GLOBAL
# ==========================================
@app.before_request
def verificar_autenticacao():
    # 1. Lista de endpoints que QUALQUER UM pode aceder sem estar logado
    # 'static' permite que as imagens e o CSS carreguem na tela de login/cadastro
    rotas_publicas = ['login_page', 'cadastro_page', 'processar_login', 'processar_cadastro', 'static']

    # 2. Se a rota atual exigir login e o utilizador NÃO estiver autenticado, barra o acesso!
    if request.endpoint not in rotas_publicas and 'usuario_logado' not in session:
        flash("Acesso negado! Por favor, faça login primeiro.", "warning")
        return redirect(url_for('login_page'))


# ==========================================
# ROTAS DE AUTENTICAÇÃO (PROCESSAMENTO)
# ==========================================

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
        return redirect(url_for('index')) 
        
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
        flash("Cadastro realizado com sucesso! Faça seu login.", "success")
        return redirect(url_for('login_page'))
    else:
        flash("Erro no cadastro! Verifique seus dados ou se o CPF/E-mail já existem.", "danger")
        return redirect(url_for('cadastro_page'))


# ==========================================
# ROTAS DE RENDERIZAÇÃO DE PÁGINAS (HTML)
# ==========================================

# A rota raiz (/) e (/index) estão seguras por causa do before_request
@app.route('/')
@app.route('/index')
def index():
    email_logado = session.get('usuario_logado')
    return render_template('index.html', usuario=email_logado)


@app.route('/agendamento')
def agendamento_page():
    email_logado = session.get('usuario_logado')
    return render_template('agendamento.html', usuario=email_logado)


@app.route('/quem-somos')
def quem_somos_page():
    return render_template('quem-somos.html')


@app.route('/servicos')
def servicos_page():
    return render_template('servicos.html')


@app.route('/marketplace')
def marketplace_page():
    return render_template('marketplace.html')


# Estas duas rotas estão listadas em 'rotas_publicas', logo o Flask não as bloqueia
@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastro.html')


# ==========================================
# ROTAS DE AGENDAMENTO (PROCESSAMENTO)
# ==========================================

@app.route('/agendar_pelo_site', methods=['POST'])
def receber_agendamento_do_site():
    if 'usuario_logado' not in session:
        return "Erro: Usuário não autenticado.", 401

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
    return resposta_do_banco


# ==========================================
# ROTA DE LOGOUT
# ==========================================
@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)