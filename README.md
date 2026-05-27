# Projeto Prospeccao B2B

<!-- Comentario geral: este README apresenta o projeto em passos curtos: primeiro o objetivo, depois a estrutura, os requisitos atendidos e por fim como executar. -->

Sistema web em Flask organizado em MVC para prospeccao de vendas B2B com PostgreSQL, consulta de CNPJ via BrasilAPI, funil de leads, historico de interacoes e modulo administrativo.

## Estrutura

```text
.
+-- prospeccao_b2b/
|   +-- controllers/              # Entrada HTTP, permissoes e renderizacao
|   +-- models/                   # Acesso ao PostgreSQL
|   +-- services/                 # Regras de negocio e integracoes
|   +-- templates/                # Views HTML
|   +-- static/                   # CSS
|   +-- app.py                    # Ponto de entrada
|   +-- init_db.py                # Cria tabelas e admin inicial
|   +-- schema.sql                # Schema PostgreSQL da aplicacao
+-- database/
|   +-- schema.sql                # Copia do schema principal
|   +-- indexes.sql               # Indices separados para consulta
+-- RUN_SYSTEM.txt                # Passo a passo para rodar
+-- requirements.txt
```

## Requisitos atendidos

- Login/logout com controle de sessao.
- Endpoints JWT com refresh token para clientes API.
- Recuperacao de senha com token temporario.
- Busca de empresa por CNPJ na BrasilAPI.
- Filtros por CNAE, capital social, porte, UF, municipio e situacao.
- Funil com os status: Lead Novo, Em Contato, Negociando, Cliente e Rejeitado.
- Consultor ve apenas seus proprios leads.
- Administrador ve todos os leads, gerencia usuarios e acessa relatorio global.
- Registro, listagem e edicao de interacoes em ate 24h.
- Exclusao de interacoes restrita ao administrador.
- Senhas armazenadas com hash bcrypt.
- Queries parametrizadas com psycopg para reduzir risco de SQL Injection.

## Como rodar

Veja o arquivo `RUN_SYSTEM.txt`.
