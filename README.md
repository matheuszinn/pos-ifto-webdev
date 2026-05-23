# Agenda Pro - Agenda Inteligente Integrada ao Gemini

Agenda Pro é uma aplicação web moderna que combina o gerenciamento tradicional de calendário com a potência da Inteligência Artificial (Google Gemini). O sistema permite que os usuários criem eventos via linguagem natural, gerem rotinas complexas automaticamente e mantenham sua vida organizada de forma inteligente.

Esta versão inclui uma interface robusta, acessível e totalmente responsiva.

## 🚀 Funcionalidades Principais

- **Agendamento Mágico (IA):** Digite "Reunião amanhã às 14h" e a IA estrutura o evento para você.
- **Geração de Rotinas (IA):** Gere planos de estudo ou exercícios para vários dias com um único clique.
- **Calendário Interativo:** Visualize seus compromissos em visualizações de Mês, Semana, Dia ou Lista.
- **Interface Responsiva:** Otimizada para Desktop, Tablet e Mobile.
- **UX & Acessibilidade:** Navegação por teclado, feedbacks visuais de carregamento e validações em tempo real.
- **Performance:** Sistema de cache inteligente para carregamento rápido de eventos.
- **Autenticação Completa:** Sistema de cadastro e login seguro com hash de senhas.

---

## 🛠️ Pré-requisitos

- **Python 3.11 ou superior**
- Uma conta no [Google AI Studio](https://aistudio.google.com/) para obter uma `GEMINI_API_KEY`.
- **Make** (opcional, para usar os comandos do Makefile).

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
```

### 3. Instalar dependências e Makefile
```bash
make install
```

### 4. Configurar variáveis de ambiente
Crie um arquivo chamado `.env` na raiz do projeto:
```env
FLASK_ENV=development
DATABASE_URL=sqlite:///agenda.db
GEMINI_API_KEY=SUA_CHAVE_AQUI
GEMINI_MODEL_NAME=gemini-pro
```

---

## 🏃 Executando a Aplicação

Para iniciar o servidor:
```bash
make run
```
Acesse: [http://127.0.0.1:5001](http://127.0.0.1:5001)

---

## 🧪 Testes e Validação

### Testes Automatizados (pytest)
```bash
make test
```

### Teste de Fumaça (Docker + Smoke Test)
```bash
make docker-build
make docker-run
make smoke-test
```

---

## 🧰 Tecnologias Utilizadas

- **Backend:** Flask, Flask-SQLAlchemy (SQLite), Flask-Caching.
- **IA:** Google Generative AI (Gemini Pro).
- **Frontend:** Jinja2, Bootstrap 5, FullCalendar 6.
- **Testes:** Pytest, Pytest-Mock.
- **Infra:** Docker, Makefile.
