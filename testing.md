# Plano de Testes - Agenda Pro (V2)

Este documento descreve a estratégia de testes automatizados e manuais para validar a integridade do sistema Agenda Pro, com foco em robustez, backend e experiência de usuário (UX).

## 1. Estratégia de Teste
- **Testes Unitários:** Validação exaustiva de `UserService` e `CalendarService`.
- **Testes de Integração:** Validação das rotas Flask (MTV e JSON API).
- **Testes de Frontend (Manuais/E2E):** Validação de UI, responsividade e acessibilidade.
- **Mocks:** Simulação da API do Gemini para testes determinísticos.

## 2. Cenários de Teste Backend

### 2.1 Usuário e Autenticação
- **Registro:** Sucesso, Falha (Email duplicado), Falha (Email inválido), Falha (Senha curta).
- **Autenticação:** Sucesso, Falha (Senha incorreta), Falha (Usuário inexistente).
- **Segurança:** Proteção de rotas via login e retorno de 401 para APIs protegidas.

### 2.2 Gerenciamento de Agenda
- **Eventos:** Criar (Sucesso), Falha (Cronologia), Editar (Ownership), Deletar (Ownership).

### 2.3 Inteligência Artificial
- **Extração/Rotina:** Simular respostas variadas do Gemini (JSON limpo, markdown, lista, erro).

## 3. Cenários de Teste Frontend (UX/UI)

### 3.1 Responsividade
- **Cenário Mobile:** Validar que a Navbar colapsa e o calendário ajusta a visualização para dispositivos pequenos.
- **Cenário Tablet:** Validar que o layout em coluna única funciona sem quebra de elementos.

### 3.2 Estados de Feedback
- **Carregamento:** Clicar em "Processar com IA" e verificar se o botão desabilita ou exibe spinner.
- **Mensagens:** Verificar se erros de validação aparecem como alertas flutuantes claros.
- **Validação Visual:** Tentar submeter formulários vazios e verificar o feedback `is-invalid` do Bootstrap.

### 3.3 Acessibilidade
- **Teclado:** Navegar por toda a aplicação usando apenas `Tab` e `Enter`. Verificar se o foco é visível.
- **Leitores de Tela:** Validar a presença de `aria-label` em botões de ação e ícones.

## 4. Execução dos Testes
### Backend (Automatizado)
```bash
pytest
```
### Frontend (Manual/Smoke)
1.  Rodar a aplicação: `make run`
2.  Acessar `http://localhost:5001`
3.  Executar fluxo de cadastro -> login -> agendamento IA -> edição.
4.  Redimensionar a janela do navegador para testar responsividade.
