# Agenda Pro - Agenda Inteligente Integrada ao Gemini

Agenda Pro é uma aplicação web moderna que combina o gerenciamento tradicional de calendário com a potência da Inteligência Artificial (Google Gemini). O sistema permite que os usuários criem eventos via linguagem natural, gerem rotinas complexas automaticamente e mantenham sua vida organizada de forma inteligente.

Esta versão inclui uma interface robusta, acessível e totalmente responsiva, com processamento assíncrono de IA e cache de performance.

## 🚀 Funcionalidades Principais

- **Agendamento Mágico (IA):** Digite "Reunião amanhã às 14h" e a IA estrutura o evento para você.
- **Geração de Rotinas (IA):** Gere planos de estudo ou exercícios para vários dias em segundo plano.
- **Calendário Interativo:** Visualize compromissos em visualizações de Mês, Semana, Dia ou Lista.
- **Interface Responsiva:** Otimizada para Desktop, Tablet e Mobile.
- **UX & Acessibilidade:** Navegação por teclado, feedbacks visuais de carregamento (spinners) e validações em tempo real.
- **Performance:** Sistema de cache inteligente (Flask-Caching) e processamento assíncrono (Threading).
- **Autenticação Completa:** Sistema de cadastro e login seguro com hash de senhas e validação de e-mail.

---

## 🛠️ Pré-requisitos

- **Python 3.11 ou superior**
- Uma conta no [Google AI Studio](https://aistudio.google.com/) para obter uma `GEMINI_API_KEY`.
- **Make** instalado no sistema.
- **Docker** (opcional, para testes de fumaça em container).

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:

| Variável | Descrição | Exemplo |
| :--- | :--- | :--- |
| `FLASK_ENV` | Ambiente de execução (`development` ou `production`). | `development` |
| `SECRET_KEY` | Chave para sessões (opcional, possui default para dev). | `minha_chave_secreta` |
| `DATABASE_URL` | URL de conexão do SQLite. | `sqlite:///agenda.db` |
| `GEMINI_API_KEY` | Sua chave de API do Google Gemini. | `AIzaSy...` |
| `GEMINI_MODEL_NAME` | Nome do modelo do Gemini a ser utilizado. | `gemini-pro` |

---

## 📦 Configuração e Execução

### 1. Preparar Ambiente
```bash
make install
```

### 2. Rodar Aplicação
```bash
make run
```
Acesse: [http://127.0.0.1:5001](http://127.0.0.1:5001)

---

## 🧪 Comandos de Build e Teste

Utilize o `Makefile` para gerenciar o ciclo de vida do projeto:

- **Instalação:** `make install`
- **Execução:** `make run`
- **Testes Unitários/Integração:** `make test`
- **Build Docker:** `make docker-build`
- **Executar Docker:** `make docker-run`
- **Limpar Docker:** `make docker-clean`
- **Smoke Test:** `make smoke-test` (Valida o container rodando)

---

## 🧰 Stack Tecnológica

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Caching, python-dotenv.
- **IA:** Google Generative AI (Gemini SDK).
- **Frontend:** Jinja2, Bootstrap 5, FullCalendar 6, Bootstrap Icons.
- **Testes:** Pytest, Pytest-Mock, Requests (smoke test).
- **Infra:** Docker, Makefile.
