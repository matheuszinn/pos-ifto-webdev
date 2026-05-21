O presente documento detalha a descrição do projeto para o sistema de "Agenda Inteligente Integrada ao Gemini" (Agenda Pro), conforme as especificações de plataforma tecnológica, arquitetura e requisitos de usuário.1. Definir Usuários: Cliente

**Nome do Usuário:** Cliente

**Definição:** O Cliente é o usuário final da aplicação, que se cadastra de forma autônoma (self-registration) para gerenciar sua agenda e interagir com os serviços de inteligência artificial.

**Casos de Uso Principais:**

* **CRUD de Usuário:** Criação, leitura, atualização e exclusão do próprio perfil de usuário.  
* **Agendamento:** Adicionar e Consultar anotações no calendário.  
* **Interação com IA:** Promptar anotações para estruturação automática e Formular rotinas com base em sugestões (estudo ou exercício).

2\. Arquitetura

O sistema será implementado sob uma arquitetura de Três Camadas, utilizando o padrão Modelo-Template-Visão (MTV) nativo do Flask. A aplicação é modularizada para isolar o core do backend (lógica de negócio e dados) da camada de integração com a IA.

* **Camada de Apresentação (Frontend):** Interface de usuário construída com HTML renderizado pelo **Jinja2** e estilizada pelo **Bootstrap**. Responsável pela interação direta do Cliente, recebendo dados de agendamento e *prompts* de IA.  
* **Camada de Lógica de Aplicação (Backend):** Desenvolvida em **Python** utilizando o framework **Flask**. Contém a lógica de negócio, autenticação, gerenciamento de sessões e o módulo de serviço de IA.  
* **Camada de Dados (Persistência):** Utiliza o **SQLite** como banco de dados relacional para armazenar dados de usuários, eventos e anotações.  
* **Infraestrutura:** A aplicação inteira será empacotada em um **Container Docker**, facilitando o deployment e garantindo que o ambiente de execução seja consistente.

3\. Plataforma Tecnológica

A plataforma é definida com foco em agilidade de desenvolvimento e integração com serviços de IA.

| Componente | Tecnologia | Finalidade |
| ----- | ----- | ----- |
| **Linguagem** | Python | Linguagem principal de desenvolvimento do backend e integração da API. |
| **Framework Web** | Flask | Framework minimalista para gerenciar rotas, requisições HTTP e controle de fluxo da aplicação. |
| **Template Engine** | Jinja 2 | Renderização dinâmica dos templates HTML, permitindo a exibição de dados do backend no frontend. |
| **Frontend/UI** | Bootstrap | Framework CSS para desenvolvimento de uma interface de usuário responsiva e moderna. |
| **Banco de Dados** | SQLite | Banco de dados leve e baseado em arquivo, ideal para prototipagem e o escopo inicial do projeto. |
| **Containerização** | Docker | Empacotamento do ambiente de execução (Flask/Python) em um container para portabilidade. |
| **Controle de Versão** | GitHub | Controlador de versões distribuído para o código-fonte, conectado a uma conta online para colaboração e *backup*. |

4\. Estrutura de Diretórios

A estrutura de diretórios adota a convenção de aplicações Flask para organizar módulos, templates e arquivos estáticos, mantendo a aplicação limpa e escalável.

```
agenda_pro/
├── app/
│   ├── static/             # Arquivos estáticos (CSS, JS, Imagens, Bootstrap)
│   ├── templates/          # Templates HTML renderizados pelo Jinja2
│   ├── __init__.py         # Inicialização da aplicação Flask
│   ├── models.py           # Definição das classes de dados (Tabelas do SQLite)
│   ├── routes.py           # Definição das rotas HTTP (Controladores)
│   └── services/           # Lógica de negócio e integração de módulos
│       ├── user_service.py # Gerencia CRUD de usuário e autenticação
│       └── ai_gemini_service.py # Integração e chamadas à API Gemini
├── venv/                   # Ambiente virtual Python
├── tests/                  # Diretório para testes unitários
├── .gitignore              # Ignora arquivos desnecessários (venv, cache)
├── Dockerfile              # Definição de construção da imagem Docker
├── requirements.txt        # Lista de dependências Python (Flask, etc.)
└── config.py               # Arquivo de configuração e variáveis de ambiente
```

5\. Convenções

As convenções são estabelecidas para garantir a manutenção e a legibilidade do código.

* **Estilo de Código:** Seguir o padrão **PEP 8** (Python Enhancement Proposal 8\) para formatação de código Python.  
* **Nomenclatura:**  
  * Variáveis e Funções: Utilizar `snake_case` (ex: `adicionar_evento`).  
  * Classes e Módulos: Utilizar `CamelCase` (ex: `UserService`, `CalendarEvent`).  
* **Documentação:** Utilizar **docstrings** em todas as funções e métodos para descrever propósito, parâmetros e retorno.  
* **Commits Git:** Utilizar mensagens de *commit* descritivas e padronizadas (ex: `feat: adiciona formulario de cadastro`).  
* **Templates Jinja2:** Utilizar *include* e *extends* para evitar repetição de código HTML.

6\. Serviços (Módulos)

Os serviços encapsulam a lógica de negócio necessária para atender aos casos de uso definidos.

* **`UserService`:** Gerencia todas as operações de **CRUD de usuário**. Responsável pela lógica de auto-cadastro, hash de senhas e autenticação (login/logout).  
* **`CalendarService`:** Gerencia a persistência dos dados da agenda no SQLite. Inclui métodos para **Adicionar anotações ao calendário** e **Consultar as anotações do calendário**.  
* **`AIGeminiService`:** Módulo de integração com a API Gemini.  
  * **Processamento de Anotações:** Recebe o *prompt* do usuário e utiliza a IA para analisar o texto, extrair data, hora e descrição, e retornar o evento estruturado para o `CalendarService`.  
  * **Geração de Rotinas:** Recebe o pedido do usuário ("rotina de exercício/estudo") e utiliza a IA para **Formular rotinas com base em sugestões**, gerando uma lista de tarefas agendáveis.

7\. Variáveis de Ambiente

As variáveis de ambiente são necessárias para a configuração da aplicação e para a segurança, sendo injetadas pelo **Docker** no ambiente de execução.

| Variável | Descrição | Exemplo de Valor (Dev) |
| ----- | ----- | ----- |
| `FLASK_ENV` | Define o ambiente de execução (`development` ou `production`). | `development` |
| `SECRET_KEY` | Chave criptográfica usada para assinar cookies de sessão e garantir a segurança. | `uma_chave_secreta_forte` |
| `DATABASE_URL` | Caminho de conexão para o banco de dados SQLite. | `sqlite:///agenda.db` |
| `GEMINI_API_KEY` | Chave de autenticação necessária para se comunicar com a API do Gemini. | `AIzaSy...` |
| `GEMINI_MODEL_NAME` | Nome do modelo específico do Gemini a ser usado para *prompting* e geração de rotinas. | `gemini-pro` |

A partir da descrição do sistema acima, gere a respectiva especificação.  
4\. Especificação (Spec)

4.1  
Formato:  
/path/do/arquivo

- ação: criar | modificar | consultar  
- descrição  
- pseudocódigo

4.2 As especificações devem ser

* Determinística  
* Granulares  
* Sem ambiguidadesEspecificação (Spec)

4.1 Formato:

```
/path/do/arquivo
- ação: criar | modificar | consultar
- descrição
- pseudocódigo
```

4.2 As especificações devem ser Determinísticas, Granulares e Sem ambiguidades.-----**Especificações do Módulo de Inicialização e Dados**

**/app/\_\_init\_\_.py**

* ação: criar  
* descrição: Inicializa a aplicação Flask, carrega as configurações do ambiente (`config.py`) e inicializa o banco de dados SQLite.  
* pseudocódigo:

```
FUNÇÃO create_app(config_object):
    APP = Flask(__name__)
    APP.config.from_object(config_object)
    DB.init_app(APP)
    REGISTRAR rotas (app/routes.py)
    
    RETORNAR APP
    
FUNÇÃO initialize_database():
    SE o arquivo DATABASE_URL não existir:
        CRIAR tabelas definidas em app/models.py
        INFORMAR SUCESSO
```

**/config.py**

* ação: criar  
* descrição: Define a classe de configuração, carregando variáveis de ambiente (como `SECRET_KEY` e `GEMINI_API_KEY`).  
* pseudocódigo:

```
CLASSE Config:
    SECRET_KEY = OS.ENV.get('SECRET_KEY')
    FLASK_ENV = OS.ENV.get('FLASK_ENV', 'development')
    SQLALCHEMY_DATABASE_URI = OS.ENV.get('DATABASE_URL', 'sqlite:///agenda.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = FALSE
    GEMINI_API_KEY = OS.ENV.get('GEMINI_API_KEY')
    GEMINI_MODEL_NAME = OS.ENV.get('GEMINI_MODEL_NAME', 'gemini-pro')
```

**/app/models.py**

* ação: criar  
* descrição: Definição dos modelos de banco de dados para Usuário (`User`) e Evento/Anotação (`CalendarEvent`).  
* pseudocódigo:

```
CLASSE User(DB.Model):
    id: INTEGER PRIMARY KEY
    email: STRING(120) UNIQUE NOT NULL
    password_hash: STRING(128) NOT NULL
    created_at: DATETIME DEFAULT NOW
    
    FUNÇÃO set_password(password):
        self.password_hash = generate_hash(password)
    
    FUNÇÃO check_password(password):
        RETORNAR check_hash(self.password_hash, password)

CLASSE CalendarEvent(DB.Model):
    id: INTEGER PRIMARY KEY
    user_id: INTEGER FOREIGN KEY (referencia User.id)
    title: STRING(100) NOT NULL
    description: TEXT
    start_time: DATETIME NOT NULL
    end_time: DATETIME
    is_ai_generated: BOOLEAN DEFAULT FALSE
```

**Especificações do Módulo de Usuário (UserService)**

**/app/services/user\_service.py**

* ação: criar  
* descrição: Lógica de negócio para o auto-cadastro (criação) do cliente.  
* pseudocódigo:

```
FUNÇÃO register_user(email, password):
    SE User.query.filter_by(email=email).first() EXISTE:
        RETORNAR Erro: "Usuário já cadastrado"
    
    NOVO_USUARIO = User(email=email)
    NOVO_USUARIO.set_password(password)
    SALVAR(NOVO_USUARIO)
    
    RETORNAR SUCESSO, NOVO_USUARIO
```

* ação: consultar  
* descrição: Autentica o usuário para login.  
* pseudocódigo:

```
FUNÇÃO authenticate_user(email, password):
    USUARIO = User.query.filter_by(email=email).first()
    
    SE USUARIO EXISTE E USUARIO.check_password(password) É VERDADEIRO:
        RETORNAR SUCESSO, USUARIO
    SENÃO:
        RETORNAR Erro: "Credenciais inválidas"
```

**Especificações do Módulo de Calendário (CalendarService)**

**/app/services/calendar\_service.py**

* ação: criar  
* descrição: Cria um novo evento na agenda, seja ele inserido manualmente ou gerado pela IA.  
* pseudocódigo:

```
FUNÇÃO add_event(user_id, title, description, start_time, end_time, is_ai_generated=FALSE):
    NOVO_EVENTO = CalendarEvent(
        user_id=user_id, 
        title=title, 
        description=description, 
        start_time=start_time, 
        end_time=end_time, 
        is_ai_generated=is_ai_generated
    )
    SALVAR(NOVO_EVENTO)
    
    RETORNAR NOVO_EVENTO
```

* ação: consultar  
* descrição: Busca e retorna todos os eventos do calendário de um usuário, ordenados por data e hora.  
* pseudocódigo:

```
FUNÇÃO get_user_events(user_id, start_date=None, end_date=None):
    QUERY = CalendarEvent.query.filter_by(user_id=user_id)
    
    SE start_date e end_date FOREM FORNECIDOS:
        QUERY = QUERY.filter(CalendarEvent.start_time.between(start_date, end_date))
        
    EVENTOS = QUERY.order_by(CalendarEvent.start_time).all()
    
    RETORNAR LISTA DE EVENTOS
```

**Especificações do Módulo de IA (AIGeminiService)**

**/app/services/ai\_gemini\_service.py**

* ação: modificar (formatação de dados)  
* descrição: Comunica-se com a API Gemini para processar um texto livre (*prompt*) e extrair os campos estruturados de um evento (título, descrição, data/hora).  
* pseudocódigo:

```
FUNÇÃO process_annotation_prompt(user_prompt):
    PROMPT_SISTEMA = "Você é um assistente de agendamento. Dada a anotação do usuário, retorne um objeto JSON estrito com os campos 'title', 'description', 'start_time' (formato ISO 8601) e 'end_time' (formato ISO 8601). Inferir a data/hora se não for explícito."
    
    CHAMAR API GEMINI(
        modelo=ENV.GEMINI_MODEL_NAME, 
        system_instruction=PROMPT_SISTEMA, 
        user_input=user_prompt
    )
    
    SE API RETORNA JSON VÁLIDO:
        EVENTO_ESTRUTURADO = PARSE JSON
        RETORNAR EVENTO_ESTRUTURADO
    SENÃO:
        RETORNAR Erro: "Não foi possível estruturar a anotação"
```

* ação: criar (lista de eventos)  
* descrição: Utiliza o Gemini para gerar uma rotina complexa (ex: estudo, exercício) em formato de lista de eventos estruturados.  
* pseudocódigo:

```
FUNÇÃO generate_routine_and_save(user_id, routine_type, context):
    PROMPT_IA = "Gerar uma rotina de " + routine_type + " para 7 dias, considerando o contexto: " + context + ". Retornar uma lista JSON de eventos/tarefas com 'title', 'description', 'start_time' e 'end_time'."
    
    CHAMAR API GEMINI(modelo, PROMPT_IA)
    
    SE API RETORNA LISTA JSON VÁLIDA:
        LISTA_DE_EVENTOS = PARSE JSON
        NOVOS_IDS = []
        
        PARA CADA evento EM LISTA_DE_EVENTOS:
            NOVO_EVENTO = CalendarService.add_event(
                user_id=user_id, 
                title=evento.title, 
                start_time=evento.start_time, 
                ..., 
                is_ai_generated=TRUE
            )
            NOVOS_IDS.APPEND(NOVO_EVENTO.id)
        
        RETORNAR SUCESSO, NOVOS_IDS
    SENÃO:
        RETORNAR Erro: "Falha na geração da rotina pela IA"
```

  