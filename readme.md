# Biblioteca Digital API

API REST para gerenciamento de uma biblioteca digital, desenvolvida em Python, com foco em validações e regras de negócio.  
O sistema permite o cadastro e a consulta de usuários e livros, além do controle completo do ciclo de empréstimos da biblioteca, incluindo cálculo automático de multas por atraso e consulta do histórico de empréstimos.

---

## Visão Geral

Este projeto foi desenvolvido como um case técnico, com o objetivo de demonstrar:

- modelagem de domínio
- aplicação de regras de negócio
- separação clara de responsabilidades
- organização de código em camadas
- boas práticas de desenvolvimento de APIs REST

O foco do projeto está na **clareza das regras de negócio**, **organização do código** e **facilidade de manutenção**, priorizando soluções simples e bem estruturadas.

---

## Instruções de Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior
- Git

---

### Instalação

Clone o seguinte repositório

```
bash
git clone https://github.com/Addllleer/bibliotecaAd
cd bibliotecaAd
```

### Criar a ativar o ambiente virtual
#### Linux / macOS:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows (Git Bash / Powershell): 
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Execução
em desenvolvimento

#### Cenários de teste
Exemplos de casos de uso (cenários):
- Listar todos os usuários
- Cadastrar novos usuários
- Buscar usuário por id do usuário
- Listar todos os empréstimos associados a um usuário
- Listar todos os livros da biblioteca
- Cadastrar novo livro vinculado a um autor
- Verificar disponibilidade de um livro para empréstimo
- Realizar o empréstimo de um livro
- Processar devolução com cálculo de multa
- Listar todos os empréstimos ativos e atrasados
- Consultar histórico de empréstimos por usuário

Testes manuais via Insomnia ou Postman
 
Collection Insomnia será disponibilizada

## Testes
O projeto possui testes unitários focados na camada de serviços, validando as principais regras de negócio. É possível também executar e validar a aplicação localmente, incluindo testes manuais via API e testes automatizados.

Para executar os testes:

### Teste unitário:
```
pytest -v
```

---

### Teste Local da Aplicação
Com o ambiente virtual ativado, execute o comando abaixo na raiz do projeto:

```
python -m uvicorn app.main:app --reload
```

Acesse a aplicação em:
```
http://localhost:8000/docs
```

---

## Arquitetura
O projeto segue uma Arquitetura em camadas baseada em Router, Service e Repository, organizada da seguinte maneira:
- Router: recebe requisições HTTP
- Service: concentra regras de negócio e orquestra fluxos
- Repository: executa operações de persistência (CRUD)
- Database: armazena os dados da aplicação

### Routers
Camada responsável por:
- receber requisições HTTP
- validar dados de entrada (via schemas)
- delegar o processamento para os services
- retornar respostas HTTP
Não contém regra de negócio.

---

### Services
Camada central da aplicação, responsável por:
- implementar regras de negócio
- validar fluxos (ex: limite de empréstimos)
- calcular multas e prazos
- coordenar chamadas aos repositories

---

### Repositories
Responsáveis exclusivamente pelo acesso a dados. Contém:
- operações CRUD
- consultas e filtros
- contagens e buscas específicas
- Esta camada depende das camadas superiores, nunca o contrário.

---

### Models
Representam as entidades persistidas no banco de dados. Contém:
- Implementados com SQLAlchemy
- Mapeiam tabelas e relacionamentos
- Não contêm lógica de negócio

---

### Schemas
Responsável por:
- validação de dados de entrada
- formatação de respostas
- contratos de request/response
Implementados com Pydantic.

---

## Funcionalidades

### Gestão de Usuários
- Cadastrar usuário
- Buscar usuário por id_usuario
- Listar usuários
- Listar empréstimos ativos e atrasados de um usuário
- Consultar histórico completo de empréstimos de um usuário

---

### Catálogo de Livros
- Cadastrar livro
- Incrementar quantidade de cópias de um livro existente
- Listar livros disponíveis na biblioteca
- Consultar detalhes de um livro
- Verificar disponibilidade de livro para empréstimo
  - Quantidade total de cópias
  - Quantidade de cópias disponíveis

---

### Sistema de Empréstimos
- Realizar empréstimo de livro
- Validar o número de empréstimos por usuário
- Controlar prazo de devolução do empréstimo
- Processar devolução de livro
- Calcular multa automaticamente em caso de atraso
- Atualizar status do empréstimo (ativo, atrasado, devolvido)
- Listar empréstimos ativos e atrasados
- Consultar histórico de empréstimos

---

## Regras de Negócio Aplicadas
- Prazo padrão de empréstimo de **14 dias**
- Multa de **R$ 2,00 por dia de atraso**
- Limite máximo de **3 empréstimos ativos ou atrasados por usuário**
- Empréstimos atrasados continuam contando para o limite
- Prazo de devolução definido no momento do empréstimo
- Multa calculada apenas no momento da devolução

---

## Estrutura de Pastas

```text
├──app/
|  ├── main.py              # Ponto de entrada da aplicação (FastAPI)
|  ├── database.py          # Configuração e conexão com o banco de dados (SQLite)
|  ├── utils.py             # Funções utilitárias compartilhadas
|  ├── __init__.py          
|  │
|  ├── domain/enums              # Models ORM (SQLAlchemy)
|  │   ├── categoria_livro.py
|  │   ├── localizacao_livro.py
|  │   └── perfil_acesso.py
|  |
|  ├── models/              # Models ORM (SQLAlchemy)
|  │   ├── model_emprestimo.py
|  │   ├── model_livro.py
|  │   └── model_usuario.py
|  │
|  ├── repositories/        # Camada de acesso a dados (CRUD e queries)
|  │   ├── repository_emprestimo.py
|  │   ├── repository_livro.py
|  │   └── repository_usuario.py
|  │
|  ├── routers/             # Rotas da API (FastAPI)
|  |   ├── router_emprestimo.py
|  |   ├── router_livro.py
|  |   └── router_usuario.py
|  │
|  ├── schemas/             # Schemas Pydantic (validação e contratos da API)
|  │   ├── schema_usuario.py
|  │   ├── schema_livro.py
|  │   └── schema_emprestimo.py
|  │
|  └── services/            # Camada de regras de negócio
|      ├── service_usuario.py
|      ├── service_livro.py
|      └── service_emprestimo.py
|  
├── docs/             # Demais documentos de análise do case
|   ├── analise_case
|   |  ├── passoPassoCenarios.txt
|   |  └── cenarios.png
|   └── arquitetura
|      ├── biblioteca.drawio
|      └── arquitetura.png
├── tests/                # Testes automatizados
│   ├── conftest.py
│   ├── test_emprestimo_service.py
│   ├── test_livro_service.py
│   └── test_usuario_service.py
└── README.md                   # Documentação do projeto

