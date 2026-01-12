# Biblioteca Digital API

API REST para gerenciamento de uma biblioteca digital, desenvolvida em Python, com foco em validações e regras de negócio.  
O sistema permite o cadastro e a consulta de usuários e livros, além do controle completo do ciclo de empréstimos da biblioteca, incluindo cálculo automático de multas por atraso e consulta do histórico de empréstimos.


## Visão Geral

Este projeto foi desenvolvido como um case técnico com o objetivo de demonstrar:
- modelagem de domínio
- aplicação de regras de negócio
- boas práticas de organização e manutenção de código
- arquitetura de software em camadas

## Instruções de Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior
- Git

---

### Instalação 
```
bash
git clone <https://github.com/Addllleer/bibliotecaAd>
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
em desenvolvimento
URL de acesso 
Collection insomnia

## Arquitetura
O projeto segue uma Clean Architecture simplificada, organizada nas seguintes camadas:
- Arquitetura em camadas (Clean Architecture simplificada)
- Separação clara entre domínio, aplicação, infraestrutura e API
- Regras de negócio centralizadas nos casos de uso
- Entidades de domínio desacopladas de frameworks
- Repositórios definidos por interfaces

### Domain
Camada responsável por representar o domínio do negócio.

Contém:
- Entidades (`Livro`, `Usuário`, `Empréstimo`)
- Enums (categoria de livro, status de empréstimo, perfil de acesso)
- Exceções de domínio

Esta camada não possui dependência de frameworks, banco de dados ou interface HTTP.

---

### Application
Camada responsável pelos casos de uso da aplicação.

Contém:
- Orquestração das regras de negócio
- Validações de fluxo
- Interfaces (contratos) de repositórios

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

### Infrastructure
Camada responsável por detalhes técnicos.

Contém:
- Modelos de banco de dados
- Implementações concretas dos repositórios
- Configuração de persistência

Esta camada depende das camadas superiores, nunca o contrário.

---

### API
Camada responsável pela interface HTTP.

Contém:
- Rotas da API
- Schemas de entrada e saída
- Conversão de exceções de domínio para respostas HTTP

Nenhuma regra de negócio é implementada nesta camada.

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
src/
├── api/
│   ├── routers/
│   └── schemas/
├── application/
│   ├── interfaces/
│   └── use_cases/
├── domain/
│   ├── entities/
│   ├── enums/
│   └── exceptions/
├── infrastructure/
│   ├── database/
│   │   └── models/
│   └── repositories/
└── main.py
