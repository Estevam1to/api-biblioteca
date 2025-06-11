# API Biblioteca - Sistema de Gerenciamento

Sistema completo de gerenciamento de biblioteca desenvolvido com FastAPI, SQLModel e Alembic.

## Funcionalidades

- **CRUD completo** para todas as entidades (Autor, Editora, Livro, Usuário, Empréstimo)
- **Relacionamentos**: 1:1, 1:N e N:N entre entidades
- **Paginação** e filtros avançados
- **Sistema de logs** para monitoramento
- **Migrações** de banco com Alembic
- **Validação** de dados com Pydantic

## Entidades

1. **Autor**: Dados dos autores dos livros
2. **Editora**: Informações das editoras
3. **Livro**: Catálogo de livros
4. **Usuário**: Usuários da biblioteca
5. **Empréstimo**: Controle de empréstimos (N:N com Livros)

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar banco (opcional - usar PostgreSQL)
cp .env.example .env

# Executar migrações
alembic upgrade head

# Iniciar servidor
python run.py
```

## Endpoints Principais

- `GET /docs` - Documentação interativa
- `POST /autores/` - Criar autor
- `GET /autores/` - Listar autores
- `GET /livros/?titulo=python` - Buscar livros por título
- `POST /emprestimos/` - Criar empréstimo
- `PUT /emprestimos/{id}/devolver` - Devolver empréstimo

## Consultas Implementadas

- Busca por ID
- Filtros por relacionamentos
- Busca por texto parcial
- Filtros por data/ano
- Agregações e contagens
- Ordenações
- Consultas complexas com múltiplas entidades

## Equipe

Projeto desenvolvido por:

- **Luís Estevam**: Endpoints de autores e editoras, sistema de paginação e filtros, configuração do Alembic e estruturação do repositório.
- **Luis Fernando**: Endpoints e lógica de empréstimos, sistema de relacionamentos N:N, validações de negócio e sistema de logs.

> **Nota**: O repositório contém commits principalmente de um integrante pois ele foi responsável pela estruturação do código. O desenvolvimento foi realizado em conjunto utilizando compartilhamento de arquivos.
