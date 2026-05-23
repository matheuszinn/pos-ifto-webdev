# Especificação Técnica - Agenda Pro (V2)

Este documento detalha os requisitos, arquitetura e especificações técnicas do sistema Agenda Pro, visando robustez, manutenibilidade, clareza e uma experiência de usuário (UX) de alta qualidade.

## 1. Definição de Usuários
- **Cliente:** Usuário final que gerencia sua própria agenda. Realiza cadastro autônomo e interage com os serviços de IA.

## 2. Arquitetura e Fluxo de Dados
O sistema utiliza o padrão **MTV (Model-Template-View)** com Flask, organizado em três camadas:
1.  **Camada de Apresentação:** Templates Jinja2 + Bootstrap 5 + FullCalendar 6.
2.  **Camada de Lógica (Services):** Encapsula a inteligência do negócio e integrações externas (Gemini).
3.  **Camada de Dados:** SQLite via SQLAlchemy.

### Fluxo de Comunicação
- O Frontend interage via **Formulários Tradicionais** (com redirecionamentos e flash messages) e via **Interações Assíncronas (futuro)** para feedbacks dinâmicos.

## 3. Especificação de Frontend

### 3.1 Design System e Consistência Visual
- **Paleta de Cores:** Primária (Azul Bootstrap), Sucesso (Verde Bootstrap), Perigo (Vermelho Bootstrap), Aviso (Amarelo Bootstrap).
- **Tipografia:** Fonte padrão do sistema (Sans-serif) via Bootstrap.
- **Espaçamento:** Uso consistente das classes utilitárias `p-*` e `m-*` do Bootstrap.
- **Componentes:** Card, Modal, Alerts, Navbar, e Dropdown padronizados.

### 3.2 Estados de Tela e Feedback
- **Loading:** Botões de IA (`Processar com IA` e `Criar Tarefas`) devem exibir um spinner ou texto de "Processando..." após o clique para evitar múltiplos envios.
- **Mensagens de Erro/Sucesso:** Uso de Alerts flutuantes (Flash messages) com cores semânticas.
- **Estado Vazio:** O calendário deve renderizar corretamente mesmo sem eventos.
- **Validação de Formulário:** Uso de validação nativa do HTML5 (`required`, `min`, `max`) com feedback visual do Bootstrap (`is-invalid`).

### 3.3 Responsividade
- **Desktop:** Layout em duas colunas (Painel IA à esquerda, Calendário à direita).
- **Tablet (<= 992px):** Layout em coluna única. Painel IA move-se para o topo.
- **Mobile (<= 576px):** Calendário deve ajustar a visualização (ex: alternar para visualização de dia ou lista se necessário). Navbar colapsável.

### 3.4 Acessibilidade
- **Navegação por Teclado:** Todos os botões e links devem ser acessíveis via `Tab`. Modais devem capturar o foco.
- **Labels:** Todos os campos de formulário devem ter `<label>` associados.
- **Contraste:** Garantir legibilidade de texto sobre fundos coloridos (ex: botões).
- **ARIA:** Uso de `aria-label` em botões de fechar e ícones. `role="alert"` em mensagens de erro.

## 4. Especificação de Endpoints (Roteamento)

### 4.1 Autenticação e Usuário
- `GET /cadastro` | `POST /cadastro`: Exibe formulário ou processa cadastro.
- `GET /login` | `POST /login`: Exibe formulário ou processa login.
- `GET /logout`: Encerra a sessão.
- `PUT /api/user/password`: (Protegido) Atualiza a senha do usuário.
- `DELETE /api/user`: (Protegido) Remove a conta do usuário e todos os seus eventos.

### 4.2 Agenda e IA
- `GET /agenda`: Página principal do calendário.
- `POST /evento/add`: Adiciona evento via formulário.
- `POST /evento/editar/<id>`: Edita evento via formulário.
- `POST /evento/deletar`: Remove evento via formulário.
- `GET /api/events`: Retorna lista de eventos em JSON.
- `POST /api/ai/process`: Processa prompt de texto e cria evento. Retorna JSON.
- `POST /api/ai/routine`: Gera e salva rotina complexa. Retorna JSON.

## 5. Modelos de Dados (Pseudocódigo)

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

## 6. Especificações de Serviços

### UserService
- `register_user(email, password, name)`:
    - Valida e-mail único e formato.
    - Valida senha (mínimo 6 caracteres).
- `authenticate_user(email, password)`:
    - Verifica existência e hash.
- `update_password(user_id, new_password)`:
    - Valida nova senha (mínimo 6 caracteres).

### CalendarService
- `add_event(...)`: Valida cronologia. Invalida cache.
- `update_event(...)`: Valida ownership e cronologia. Invalida cache.
- `delete_event(...)`: Valida ownership. Invalida cache.

### AIGeminiService (Integração Robusta)
- `process_annotation_prompt(user_prompt)`: Extração JSON, limpeza de markdown e validação de campos.
- `generate_routine_and_save(...)`: Execução assíncrona via Threading para não bloquear o servidor.

## 7. Regras de Resposta API
- Sucesso (Criação): `201 Created` + JSON.
- Sucesso (Busca/OK): `200 OK` + JSON.
- Erro de Validação: `400 Bad Request` + `{"error": "mensagem"}`.
- Erro de Autenticação: `401 Unauthorized`.
- Erro Interno: `500 Internal Server Error`.
