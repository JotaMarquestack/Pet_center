from flask import Flask, render_template, request, redirect, url_for, flash, session
from login_cadastro import cadastrar_tutor, login_tutor

app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../frontend',
            static_url_path='')

app.secret_key = 'vet_care_projeto_faculdade2026'



@app.route('/processar_login', methods=['POST'])
def processar_login():
    email_digitado = request.form.get('email')
    senha_digitada = request.form.get('senha')
    login_valido = login_tutor(email_digitado, senha_digitada)

    print(f"TENTANDO LOGAR: {email_digitado}")
    print(f"Resultado do Banco de Dados: {login_valido}")
    
    if login_valido:
        session['usuario_logado'] = email_digitado
        return redirect(url_for('index'))
    
    else:
        return redirect(url_for('login_page'))

@app.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    dados = request.form.to_dict()
    print(f"DADOS RECEBIDOS PELO FLASK: {dados}") 

    nome = dados.get('nome')
    email = dados.get('email')

    resultado = cadastrar_tutor(nome, dados.get('cpf'), dados.get('telefone'), email, dados.get('senha'))
    
    if resultado:
        print("CADASTRO EXECUTADO COM SUCESSO.")
        return redirect(url_for('login_page'))
    else:
        print("ERRO: O banco de dados retornou FALSE. Verifique se o e-mail já existe ou se a conexão falhou.")
        return redirect(url_for('cadastro_page'))

@app.route('/')
def index():
    if 'usuario_logado' in session:
        return f"Bem-vindo, {session['usuario_logado']}! (Página em construção)"
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
