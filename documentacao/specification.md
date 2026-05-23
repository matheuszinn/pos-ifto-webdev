# Especificação Técnica - Agenda Pro (V2)

Este documento detalha os requisitos, arquitetura e especificações técnicas do sistema Agenda Pro, visando robustez, manutenibilidade e clareza.

## 1. Definição de Usuários
- **Cliente:** Usuário final que gerencia sua própria agenda. Realiza cadastro autônomo e interage com os serviços de IA.

## 2. Arquitetura e Fluxo de Dados
O sistema utiliza o padrão **MTV (Model-Template-View)** com Flask, organizado em três camadas:
1.  **Camada de Apresentação:** Templates Jinja2 + Bootstrap + FullCalendar.
2.  **Camada de Lógica (Services):** Encapsula a inteligência do negócio e integrações externas (Gemini).
3.  **Camada de Dados:** SQLite via SQLAlchemy.

### Fluxo de Comunicação
- O Frontend pode interagir via **Formulários Tradicionais** (para redirecionamentos e flash messages) ou via **JSON API** (para interações dinâmicas e testes automatizados).

## 3. Especificação de Endpoints (Roteamento)

### 3.1 Autenticação e Usuário
- `GET /cadastro` | `POST /cadastro`: Exibe formulário ou processa cadastro. Aceita JSON.
- `GET /login` | `POST /login`: Exibe formulário ou processa login. Aceita JSON.
- `GET /logout`: Encerra a sessão.
- `PUT /api/user/password`: (Protegido) Atualiza a senha do usuário.
- `DELETE /api/user`: (Protegido) Remove a conta do usuário e todos os seus eventos.

### 3.2 Agenda e IA
- `GET /agenda`: Página principal do calendário.
- `POST /evento/add`: Adiciona evento via formulário.
- `POST /evento/editar/<id>`: Edita evento via formulário.
- `POST /evento/deletar`: Remove evento via formulário.
- `GET /api/events`: Retorna lista de eventos em JSON.
- `POST /api/ai/process`: Processa prompt de texto e cria evento. Retorna JSON.
- `POST /api/ai/routine`: Gera e salva rotina complexa. Retorna JSON.

## 4. Modelos de Dados (Pseudocódigo)

### User
- `id`: Integer (PK)
- `email`: String (120, Unique, Not Null) - **Validação:** Deve ser um e-mail válido.
- `password_hash`: String (128, Not Null)
- `name`: String (100, Optional)

### CalendarEvent
- `id`: Integer (PK)
- `user_id`: Integer (FK -> User)
- `title`: String (100, Not Null)
- `description`: Text (Optional)
- `start_time`: DateTime (Not Null)
- `end_time`: DateTime (Optional) - **Regra:** Se fornecido, deve ser posterior a `start_time`.
- `is_ai_generated`: Boolean (Default False)

## 5. Especificações de Serviços

### UserService
- `register_user(email, password, name)`:
    - Valida e-mail único.
    - Valida formato de e-mail.
    - Valida senha (mínimo 6 caracteres).
    - Gera hash seguro.
- `authenticate_user(email, password)`:
    - Verifica existência e hash.
- `update_password(user_id, new_password)`:
    - Valida nova senha (mínimo 6 caracteres) e atualiza hash.

### CalendarService
- `add_event(user_id, title, description, start_time, end_time, is_ai_generated)`:
    - Valida se `end_time` (se existir) é posterior a `start_time`.
- `update_event(event_id, user_id, title, description, start_time, end_time)`:
    - Garante que o evento pertence ao usuário antes de alterar.
    - Valida se `end_time` (se existir) é posterior a `start_time`.
- `delete_event(event_id, user_id)`:
    - Garante que o evento pertence ao usuário antes de remover.

### AIGeminiService (Integração Robusta)
- `process_annotation_prompt(user_prompt)`:
    1. Envia prompt estruturado ao Gemini solicitando JSON estrito.
    2. **Limpeza:** Remove blocos de markdown (` ```json ` ou ` ``` `).
    3. **Parsing:** Converte para objeto. Se retornar lista, extrai o primeiro item.
    4. **Validação:** Garante campos obrigatórios (`title`, `start_time`).
- `generate_routine_and_save(...)`:
    1. Solicita lista JSON de eventos baseados em contexto e dias.
    2. Itera sobre a lista, validando cada item antes de persistir via `CalendarService`.

## 6. Regras de Resposta API
- Sucesso (Criação): `201 Created` + Objeto JSON.
- Sucesso (Busca/OK): `200 OK` + JSON.
- Erro de Validação: `400 Bad Request` + `{"error": "mensagem"}`.
- Erro de Autenticação: `401 Unauthorized` + `{"error": "mensagem"}`.
- Erro de Permissão: `403 Forbidden`.
- Erro Interno: `500 Internal Server Error`.
