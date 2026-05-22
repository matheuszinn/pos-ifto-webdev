# Plano de Testes - Agenda Pro

Este documento descreve a estratégia de testes automatizados para validar a integridade do sistema Agenda Pro, focando em cenários críticos e evitando regressões.

## 1. Estratégia de Teste
A estratégia baseia-se em Test-Driven Development (TDD) para validar a lógica de negócio e as rotas da aplicação.
- **Testes Unitários:** Validação dos serviços (`UserService`, `CalendarService`).
- **Testes de Integração:** Validação das rotas Flask e persistência no banco de dados SQLite (em memória para testes).
- **Mocks:** Utilização de mocks para simular a API do Gemini, evitando dependências externas e custos/latência desnecessários durante os testes.

## 2. Cenários Críticos (Prioritários)

### 2.1 Autenticação e Usuário
- **Registro de Novo Usuário:** Validar criação bem-sucedida e erro para e-mails duplicados.
- **Autenticação:** Validar login com credenciais corretas e falha com credenciais incorretas.
- **Acesso Protegido:** Garantir que rotas como `/dashboard` redirecionem para login se o usuário não estiver autenticado.

### 2.2 Gerenciamento de Agenda
- **Criação de Eventos:** Validar persistência de eventos manuais.
- **Consulta de Eventos:** Garantir que um usuário visualize apenas seus próprios eventos.

### 2.3 Infraestrutura (Docker)
- **Validação de Build:** Garantir que o `Dockerfile` contenha os comandos necessários para instalar dependências e expor a porta correta.

## 3. Ferramentas
- **Framework:** `pytest`
- **Mocks:** `pytest-mock`
- **Banco de Dados:** SQLite (in-memory) para isolamento.

## 4. Execução dos Testes
Os testes podem ser executados com o comando:
```bash
pytest
```
