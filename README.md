# 🐾 VetCare — Pet Center

> Sistema web institucional com agendamento online para clínica veterinária.  
> Projeto acadêmico desenvolvido em equipe seguindo o fluxo GitFlow.

---

## 📋 Sobre o Projeto

O **VetCare** é um sistema web desenvolvido para a **Pet Center**, uma clínica veterinária localizada em Recife-PE. O objetivo é digitalizar a presença da clínica, apresentar seus serviços e permitir que tutores agendem consultas e serviços online de forma simples e rápida.

---

## 🚀 Funcionalidades

- 🏠 **Home** — apresentação da clínica com depoimentos e CTA
- 👥 **Sobre Nós** — história, missão, visão, valores e galeria
- 🩺 **Equipe** — perfil dos veterinários com CRMV e especialidades
- 🛍️ **Serviços** — clínica veterinária, estética pet e vitrine do pet shop
- 📅 **Agendamento Online** — fluxo completo em 7 passos
- 🔐 **Login / Cadastro** — autenticação de tutores
- 🛒 **Marketplace** — vitrine digital de produtos
- 📍 **Contato** — mapa, horários e FAQ

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Frontend | HTML5, CSS3, Bootstrap 5.3.8 |
| Backend | Python 3.11, Flask 3.1.3 |
| Banco de dados | MongoDB (pymongo 4.17.0) |
| Autenticação | bcrypt 5.0.0 |
| Versionamento | Git + GitHub (GitFlow) |

---

## 📁 Estrutura do Projeto

```
Pet_center/
├── backend/
│   ├── app.py              # Servidor Flask e rotas
│   ├── database.py         # Conexão com MongoDB
│   ├── login_cadastro.py   # Lógica de autenticação
│   └── testes_terminal.py
├── frontend/
│   ├── imagens/            # Assets de imagem
│   ├── home.html
│   ├── login.html
│   ├── cadastro.html
│   ├── servicos.html
│   ├── marketplace.html
│   ├── quem-somos.html
│   ├── style-home.css
│   ├── style-login.css
│   ├── style-cadastro.css
│   ├── style-servicos.css
│   ├── style-marketplace.css
│   └── style-quemsomos.css
├── requirements.txt
└── README.md
```

---

## ⚙️ Como Rodar Localmente

### Pré-requisitos
- Python 3.11+
- Git

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/JotaMarquestack/Pet_center.git
cd Pet_center
```

**2. Crie e ative o ambiente virtual**
```bash
# Windows
python -m venv .venv
source .venv/Scripts/activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz com:
```
MONGO_URI=sua_string_de_conexao_mongodb
```

**5. Inicie o servidor**
```bash
python backend/app.py
```

**6. Acesse no navegador**
```
http://127.0.0.1:5000
```

---

## 🌿 GitFlow

```
main        ← Produto final (merge somente quando tudo estiver pronto)
└── dev     ← Integração (merge somente quando funcional e responsivo)
    ├── feat/header-footer
    ├── feat/marketplace
    ├── feat/login-cadastro
    ├── feat/agendamento
    ├── feat/servicos
    └── feat/sobre-nos
```

### Fluxo de trabalho

```bash
# Criar nova feature
git switch dev
git checkout -b feat/nome-da-feature

# Salvar progresso
git add .
git commit -m "feat: descrição do que foi feito"
git push origin feat/nome-da-feature

# Atualizar feature com a dev
git fetch origin
git merge origin/dev --no-edit

# Abrir PR: feat/nome → dev (marcar colegas para revisar)
```

> ⚠️ Sempre avise no grupo antes de dar push e ao abrir PR.

---

## 👨‍💻 Equipe

| Membro | Responsabilidade |
|--------|-----------------|
| Mateus de Araújo | Header, Footer, Marketplace |
| Mateus França | Login, Cadastro, Agendamento (form) |
| Pedro | Agendamento Online (fluxo completo) |
| Victor Emanuel | Agendamento Online (fluxo completo) |
| João Fernando | Serviços Oferecidos |
| Ygor | Sobre Nós + Equipe |

---

## 📄 Licença

Projeto acadêmico — todos os direitos reservados à equipe de desenvolvimento.
