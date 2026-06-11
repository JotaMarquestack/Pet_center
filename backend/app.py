import os 
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Importação das funções do seu grupo
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
    # Rotas públicas que qualquer visitante pode acessar sem login
    rotas_publicas = ['login_page', 'cadastro_page', 'processar_login', 'processar_cadastro', 'static']

    # Se a rota exigir autenticação e o usuário não estiver na sessão, barra e manda para o login
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
        session.permanent = (lembrar == 'on')
            
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
        # FLUXO FORÇADO: Loga o usuário automaticamente para vinculação do pet
        session['usuario_logado'] = email
        
        flash("Cadastro realizado com sucesso! Agora, registre o seu primeiro pet para continuar.", "success")
        return redirect(url_for('cadastro_pet_page'))
    else:
        flash("Erro no cadastro! Verifique os dados ou se o CPF/E-mail já existem.", "danger")
        return redirect(url_for('cadastro_page'))


# ==========================================
# ROTAS DE RENDERIZAÇÃO DE PÁGINAS (HTML)
# ==========================================

@app.route('/')
@app.route('/index')
def index():
    email_logado = session.get('usuario_logado')
    return render_template('index.html', usuario=email_logado)


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/cadastro')
def cadastro_page():
    return render_template('cadastro.html')


@app.route('/cadastro-pet')
def cadastro_pet_page():
    return render_template('cadastro-pet.html')


@app.route('/agendamento')
def agendamento_page():
    email_logado = session.get('usuario_logado')
    lista_pets = []

    try:
        from database import conectar_banco
        db_mongo = conectar_banco()
        
        if db_mongo is not None:
            # Busca todos os documentos na coleção 'pets' do tutor logado
            lista_pets = list(db_mongo['pets'].find({"email_tutor": email_logado}))
            
    except Exception as e:
        print(f"Erro ao buscar os pets para agendamento: {e}")
        flash("Erro ao carregar os seus pets cadastrados.", "danger")

    return render_template('agendamento.html', usuario=email_logado, pets=lista_pets)


# Nova rota para renderizar a página de sucesso após o agendamento
@app.route('/agendamento-realizado')
def agendamento_realizado_page():
    return render_template('agendamento-realizado.html')


# ==========================================
# PROCESSAMENTO DE CADASTRO DE PET & AGENDAMENTO
# ==========================================

@app.route('/processar_cadastro_pet', methods=['POST'])
def processar_cadastro_pet():
    if 'usuario_logado' not in session:
        return redirect(url_for('login_page'))
        
    email_tutor = session.get('usuario_logado')
    
    # Captura as listas de dados enviadas pelo formulário dinâmico (múltiplos pets)
    nomes = request.form.getlist("nome_pet[]")
    especies = request.form.getlist("especie[]")
    racas = request.form.getlist("raca[]")
    generos = request.form.getlist("genero[]")
    pesos = request.form.getlist("peso[]")
    cores = request.form.getlist("cor[]")

    try:
        from database import conectar_banco
        db_mongo = conectar_banco()
        
        if db_mongo is not None:
            lista_documentos_pets = []
            
            # Mapeia as listas recebidas do frontend
            for i in range(len(nomes)):
                if not nomes[i].strip():
                    continue
                    
                dados_pet = {
                    "email_tutor": email_tutor,
                    "nome_pet": nomes[i],
                    "especie": especies[i] if i < len(especies) else None,
                    "raca": racas[i] if i < len(racas) else None,
                    "genero": generos[i] if i < len(generos) else "MACHO",
                    "peso": pesos[i] if i < len(pesos) else None,
                    "cor": cores[i] if i < len(cores) else None
                }
                lista_documentos_pets.append(dados_pet)
            
            # Insere no banco se houver itens válidos na lista
            if lista_documentos_pets:
                db_mongo['pets'].insert_many(lista_documentos_pets)
                flash(f"{len(lista_documentos_pets)} pet(s) registrado(s) com sucesso!", "success")
            
            return redirect(url_for('agendamento_page'))
        else:
            flash("Erro de conexão com o banco de dados.", "danger")
            return redirect(url_for('cadastro_pet_page'))
            
    except Exception as e:
        print(f"Erro ao salvar pets: {e}")
        flash("Erro ao salvar os dados dos seus pets.", "danger")
        return redirect(url_for('cadastro_pet_page'))


@app.route('/agendar_pelo_site', methods=['POST'])
def receber_agendamento_do_site():
    if 'usuario_logado' not in session:
        return "Erro: Usuário não autenticado.", 401

    e_tutor = request.form.get("email_tutor", "").strip()
    i_pet = request.form.get("id_pet", "").strip()
    servico = request.form.get("servico")
    data_c = request.form.get("data")
    hora_c = request.form.get("hora")
    obs = request.form.get("observacoes")

    motivo_completo = f"{servico} - {obs}"
    
    # Executa a função atualizada que valida na collection 'pets'
    resposta_do_banco = agendar_consulta(e_tutor, i_pet, data_c, hora_c, motivo_completo)
    
    # Redirecionamento baseado no sucesso ou falha da operação
    if "sucesso" in resposta_do_banco.lower():
        flash(resposta_do_banco, "success")
        # REDIRECIONA DIRETAMENTE PARA O SEU NOVO ARQUIVO HTML
        return redirect(url_for('agendamento_realizado_page'))  
    else:
        flash(resposta_do_banco, "danger")
        return redirect(url_for('agendamento_page'))  # Permanece na tela exibindo o erro do banco
    


@app.route('/perfil')
def perfil_page():
    if 'usuario_logado' not in session:
        flash("Por favor, faça login para acessar o seu perfil.", "warning")
        return redirect(url_for('login_page'))
        
    email_logado = session.get('usuario_logado')
    
    try:
        from database import conectar_banco
        db_mongo = conectar_banco()
        
        if db_mongo is not None:
            # 1. Busca os dados cadastrais do tutor na coleção 'clientes'
            dados_tutor = db_mongo['clientes'].find_one({"email": email_logado})
            
            # 2. Busca todos os pets vinculados a este e-mail na coleção 'pets'
            lista_pets = list(db_mongo['pets'].find({"email_tutor": email_logado}))
            
            # Se por algum motivo o tutor não for encontrado na coleção clientes, criamos um dicionário temporário
            if not dados_tutor:
                dados_tutor = {"nome": "Usuário VetCare", "email": email_logado, "telefone": "-", "cpf": "-"}
                
            return render_template('perfil.html', tutor=dados_tutor, pets=lista_pets, usuario=email_logado)
        else:
            flash("Erro de conexão com o banco de dados.", "danger")
            return redirect(url_for('index'))
            
    except Exception as e:
        print(f"Erro ao carregar perfil: {e}")
        flash("Erro ao carregar os dados do perfil.", "danger")
        return redirect(url_for('index'))


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