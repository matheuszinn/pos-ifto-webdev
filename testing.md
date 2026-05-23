# Plano de Testes - Agenda Pro (V2)

Este documento descreve a estratégia de testes automatizados para validar a integridade do sistema Agenda Pro, focando em cenários críticos e tratamento de erros.

## 1. Estratégia de Teste
- **Testes Unitários:** Validação exaustiva de `UserService` e `CalendarService`.
- **Testes de Integração:** Validação das rotas Flask (MTV e JSON API).
- **Mocks:** Simulação da API do Gemini para testes determinísticos.

## 2. Cenários de Teste

### 2.1 Usuário e Autenticação
- **Registro:**
    - Sucesso com dados válidos.
    - Falha: E-mail já cadastrado.
    - Falha: E-mail em formato inválido.
    - Falha: Senha muito curta (menos de 6 caracteres).
- **Autenticação:**
    - Sucesso com credenciais corretas.
    - Falha: Senha incorreta.
    - Falha: Usuário inexistente.
- **Segurança:**
    - Acesso à `/agenda` sem login redireciona para `/login`.
    - Endpoints `/api/*` sem login retornam `401`.

### 2.2 Gerenciamento de Agenda
- **Eventos:**
    - Criar evento com sucesso.
    - Falha: `end_time` anterior a `start_time`.
    - Editar evento com sucesso.
    - Falha: Editar evento de outro usuário (deve retornar erro ou 404).
    - Deletar evento com sucesso.
    - Falha: Deletar evento de outro usuário.

### 2.3 Inteligência Artificial (Mocado)
- **Extração de Evento:**
    - Simular resposta JSON limpa do Gemini.
    - Simular resposta do Gemini com blocos markdown (deve limpar e parsear).
    - Simular resposta do Gemini como lista (deve extrair primeiro item).
    - Falha: Resposta JSON inválida (deve tratar graciosamente).
- **Geração de Rotina:**
    - Simular geração de múltiplos eventos e validar persistência.

## 3. Execução
```bash
pytest
```
Para testes de fumaça em ambiente Docker:
```bash
python3 smoke_test.py
```
