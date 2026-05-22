# Agenda Pro - Agenda Inteligente Integrada ao Gemini

Agenda Pro é uma aplicação web moderna que combina o gerenciamento tradicional de calendário com a potência da Inteligência Artificial (Google Gemini 2.0). O sistema permite que os usuários criem eventos via linguagem natural, gerem rotinas complexas automaticamente e mantenham sua vida organizada de forma inteligente.

## 🚀 Funcionalidades Principais

- **Autenticação Completa:** Sistema de cadastro e login seguro com hash de senhas.
- **Calendário Interativo:** Visualização semanal, mensal e diária utilizando FullCalendar 6.
- **Agendamento Mágico (IA):** Digite "Reunião amanhã às 14h" e a IA estrutura o evento para você.
- **Geração de Rotinas (IA):** Gere planos de estudo ou exercícios para vários dias com um único clique.
- **Gestão de Eventos:** CRUD completo (Criar, Editar, Deletar) com confirmações de segurança.
- **Design Responsivo:** Interface limpa baseada em Bootstrap 5.

---

## 🛠️ Pré-requisitos

- **Python 3.11 ou superior**
- Uma conta no [Google AI Studio](https://aistudio.google.com/) para obter uma `GEMINI_API_KEY`.

---

## 📦 Configuração do Ambiente

Siga os passos abaixo para rodar o projeto localmente:

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd pos-ifto-webdev
```

### 2. Criar e ativar o ambiente virtual
```bash
# No macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# No Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Crie um arquivo chamado `.env` na raiz do projeto (use o exemplo abaixo):
```env
FLASK_ENV=development
DATABASE_URL=sqlite:///agenda.db
GEMINI_API_KEY=SUA_CHAVE_AIZA_AQUI
GEMINI_MODEL_NAME=gemini-flash-lite-latest
```

### 5. Inicializar o Banco de Dados
O banco de dados SQLite será criado automaticamente ao rodar a aplicação, mas você pode forçar a criação das tabelas com:
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 -c "from app import create_app, db; app = create_app(); with app.app_context(): db.create_all()"
```

---

## 🏃 Executando a Aplicação

Para iniciar o servidor de desenvolvimento:
```bash
export FLASK_APP="app:create_app()"
flask run
```
Acesse: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Testes e Validação (TDD)

O projeto foi desenvolvido seguindo práticas de TDD. Para rodar a suíte de testes:

### Testes Automatizados (pytest)
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest
```

### Teste de Fumaça (Smoke Test)
Com o servidor Flask rodando, execute este script em outro terminal para validar o fluxo completo (API + IA):
```bash
python3 smoke_test.py
```

---

## 🐳 Docker (Opcional)

Para rodar a aplicação em um container:
```bash
docker build -t agenda-pro .
docker run -p 5000:5000 --env-file .env agenda-pro
```

---

## 🧰 Tecnologias Utilizadas

- **Backend:** Flask, Flask-SQLAlchemy (SQLite)
- **IA:** Google Generative AI (Gemini 2.0 Flash Lite)
- **Frontend:** Jinja2, Bootstrap 5, FullCalendar 6
- **Testes:** Pytest, Pytest-Mock
- **Qualidade:** TDD, PEP 8
