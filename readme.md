# Biblioteca Digital API

API REST para gerenciamento de uma biblioteca digital, desenvolvida em Python com FastAPI, com foco em regras de negócio, validações consistentes e organização de código em camadas.

O sistema permite o cadastro e consulta de usuários e livros, além do controle completo do ciclo de empréstimos da biblioteca, incluindo cálculo automático de multas por atraso e consulta de histórico de empréstimos.

---

## Visão Geral

Este projeto foi desenvolvido como um case técnico, com o objetivo de demonstrar:

- modelagem de domínio
- aplicação de regras de negócio
- separação clara de responsabilidades
- organização de código em camadas
- boas práticas de desenvolvimento de APIs REST
- Testes unitários

O foco do projeto está na clareza das regras, manutenibilidade do código e simplicidade das soluções, priorizando uma arquitetura limpa e fácil de evoluir.

---

## Tecnologias Utilizadas
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Uvicorn

---

## Instruções de Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior
- Git

---

### Instalação

Clone o seguinte repositório

```
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
O projeto possui testes unitários focados na camada de serviços, validando as principais regras de negócio. É possível também executar e validar a aplicação localmente, incluindo testes manuais via API e testes automatizados.

Para executar os testes:

### Teste unitário:
Executar testes unitários
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

Documentação automática (Swagger / OpenAPI):
```
http://localhost:8000/docs
```

---

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

---
### Testes manuais via Insomnia 
Collection Insomnia:

Além dos testes unitários, o projeto conta com uma collection do Insomnia para execução de testes manuais e validação completa da API.

A collection inclui:
- Cadastro e listagem de usuários
- Cadastro e consulta de livros
- Realização e devolução de empréstimos
- Listagem de empréstimos ativos, atrasados e histórico
- Paginação em todas as listagens

O arquivo da collection está disponível em:
docs/testes/insomnia/Insomnia_biblioteca.json

#### Para utilizar:
1. Abra o Insomnia
2. Clique em **Import/Export**
3. Selecione **Import Data**
4. Importe o arquivo JSON
---

### Evidências dos testes
O projeto conta com um roteiro formal de testes manuais e evidências documentadas.

- Roteiro: `docs/testes/PlanilhaUnificadaDeTestesBiblioteca.xlsx`
- Evidências: `docs/testes/` - cada roteiro está evidenciado em sua pasta
- Collection do Insomnia: `docs/testes/insomnia/Insomnia_biblioteca.json`

Esses testes complementam os testes unitários automatizados.


## Arquitetura
O projeto segue uma Arquitetura em camadas organizada da seguinte maneira:

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
## Roadmap
Ideias e sugestões de melhoria de código e de negócio para implementação em próximas features.
Disponível em:
docs/analise_case/roadmap.md

---

## Estrutura de Pastas

```
├──app/
|  ├── main.py              # Ponto de entrada da aplicação (FastAPI)
|  ├── database.py          # Configuração e conexão com o banco de dados (SQLite)
│  ├── exceptions.py            # Handlers globais de exceção
│  ├── logger.py                # Configuração de logging
|  ├── utils.py             # Funções utilitárias compartilhadas
|  ├── __init__.py          
|  │
|  ├── domain/enums              # Models ORM (SQLAlchemy)
│  │   └── enums/
│  │       ├── categoria_livro.py
│  │       ├── localizacao_livro.py
│  │       └── perfil_acesso.py
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
|   |  ├── cenarios.png
|   |  ├── passoPassoCenarios.txt
|   |  └── roadmap.md
|   ├── arquitetura
|   |   ├── biblioteca.drawio
|   |   └── arquitetura.png
|   └── testes
|      ├── Teste Integral
|      ├── Insomnia
|      |   └── Insomnia_biblioteca.json
|      ├── Testes emprestimos
|      ├── Testes livros
|      ├── Testes usuários
|      └── PlanilhaUnificadaDeTestesBiblioteca.xlsx
|
├── tests/                # Testes automatizados
│   ├── conftest.py
│   ├── test_emprestimo_service.py
│   ├── test_livro_service.py
│   └── test_usuario_service.py
└── README.md                   # Documentação do projeto
```
