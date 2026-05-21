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

