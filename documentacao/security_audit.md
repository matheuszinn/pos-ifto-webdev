# Auditoria de Segurança - Agenda Pro (Relatório Completo)

Este arquivo consolida todos os achados da inspeção realizada em 22/05/2026, cobrindo os níveis Superficial, Moderado e Profundo.

## 1. Resumo Executivo
| Severidade | Quantidade |
| :--- | :--- |
| Crítica | 1 |
| Alta | 4 |
| Média | 7 |
| Baixa | 3 |

### Top 5 Ações Urgentes
1. Adotar Gunicorn/WSGI no Dockerfile.
2. Implementar Flask-Limiter no Login.
3. Ativar Flask-WTF para proteção CSRF.
4. Atualizar Werkzeug e outras dependências críticas.
5. Adicionar Validação de Schema (Pydantic) nas respostas da IA.

## 2. Achados Detalhados

### [A02:2021] Servidor de Desenvolvimento em Produção (CRÍTICA)
- **Arquivo:** Dockerfile
- **Causa:** Uso de `flask run`.
- **Correção:** Alterar para `gunicorn`.

### [A07:2021] Ausência de Rate Limiting (ALTA)
- **Arquivo:** app/routes.py
- **Causa:** Rota de login exposta a força bruta.
- **Correção:** Usar `Flask-Limiter`.

### [A01:2021] Falta de Proteção CSRF (ALTA)
- **Arquivo:** app/__init__.py
- **Causa:** Formulários aceitam submissões de origens externas.
- **Correção:** Integrar `CSRFProtect`.

### [A03:2021] Dependências Vulneráveis (ALTA)
- **Arquivo:** requirements.txt
- **Causa:** Werkzeug 3.0.1 tem vulnerabilidades DoS conhecidas.
- **Correção:** Atualizar para 3.0.3+.

### [A04:2021] Algoritmo de Hash Fraco (MÉDIA)
- **Arquivo:** app/models.py
- **Causa:** PBKDF2 é vulnerável a ataques de GPU em escala.
- **Correção:** Mudar para `scrypt` ou `argon2`.

## 3. Conclusão
O projeto possui uma base sólida de proteção (autoescape do Jinja2, ORM contra SQLi), mas falha em configurações de infraestrutura e endurecimento (hardening) de APIs.
