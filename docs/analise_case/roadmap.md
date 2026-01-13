# Roadmap – Próximas Features

Este documento lista ideias de evolução da Biblioteca Digital API.
As features abaixo não fazem parte do escopo atual do projeto, mas representam caminhos naturais de crescimento da aplicação.

---
## Implementações técnicas
- Sistema de reservas de livros
- Cache para consultas frequentes (Redis/Memory)
- Rate limiting nos endpoints
- Middleware de autenticação básica
- Notificações de vencimento (email/webhook)
- Sistema de renovação de empréstimos
- Exportação de relatórios (CSV/PDF)
- Observabilidade (métricas + health check)
- Desenvolvimento de um FrontEnd para a aplicação
- Controle de acesso baseado em perfil (ADMIN / USUARIO)
- Auditoria de ações por usuário autenticado
- Fila de espera para livros indisponíveis
- Mais uma validação de entrada no cadastro do usuário (e-mail ou documento)
- Busca por título, autor ou categoria na entidade livros
- Busca por nome na entidade usuários
- Adicionar o campo de "edição" na entidade livros
- Validação de (título + autor + edição) na entidade livros (evitar repetidos)
- cadastro massivo de novos livros ou usuários (ingestão através de um arquivo)

---
## Implementações de negócio
- Bloqueio automático por excesso de atrasos
- Relatórios de inadimplência
- Busca avançada de usuários
