CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) NOT NULL CHECK (perfil IN ('ADMIN', 'CONSULTOR')),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    cnae_principal VARCHAR(20),
    cnae_descricao TEXT,
    cnaes_secundarios JSONB,
    porte VARCHAR(80),
    capital_social NUMERIC(15,2) DEFAULT 0,
    situacao VARCHAR(80),
    telefone VARCHAR(80),
    email VARCHAR(180),
    municipio VARCHAR(120),
    uf VARCHAR(2),
    logradouro TEXT,
    numero VARCHAR(40),
    bairro VARCHAR(120),
    cep VARCHAR(12),
    socios_json JSONB,
    dados_json JSONB,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    criado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    empresa_id INT NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    consultor_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL DEFAULT 'Lead Novo'
        CHECK (status IN ('Lead Novo', 'Em Contato', 'Negociando', 'Cliente', 'Rejeitado')),
    observacoes TEXT,
    criado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (empresa_id, consultor_id)
);

CREATE TABLE IF NOT EXISTS interacoes (
    id SERIAL PRIMARY KEY,
    lead_id INT NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    consultor_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('LIGACAO', 'EMAIL', 'REUNIAO', 'OUTRO')),
    descricao TEXT NOT NULL,
    data_interacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    token VARCHAR(80) UNIQUE NOT NULL,
    expira_em TIMESTAMP WITH TIME ZONE NOT NULL,
    usado_em TIMESTAMP WITH TIME ZONE,
    criado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS refresh_tokens (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    token VARCHAR(80) UNIQUE NOT NULL,
    expira_em TIMESTAMP WITH TIME ZONE NOT NULL,
    revogado_em TIMESTAMP WITH TIME ZONE,
    criado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
