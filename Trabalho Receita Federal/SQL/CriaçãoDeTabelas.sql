-- 1. Tabela de USUARIOS (Consultores e Admins)
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL, -- Atende ao requisito de segurança
    perfil VARCHAR(50) NOT NULL CHECK (perfil IN ('ADMIN', 'CONSULTOR')),
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela de EMPRESAS (Dados da Receita Federal)
CREATE TABLE empresas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    cnae_principal VARCHAR(7) NOT NULL,
    porte VARCHAR(50),
    capital_social NUMERIC(15,2) DEFAULT 0.00,
    uf CHAR(2),
    municipio VARCHAR(100),
    status_rfb VARCHAR(50) DEFAULT 'ATIVA', -- Fundamental para o descarte automático
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabela de LEADS (O funil da Fabiana)
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    consultor_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'PENDENTE' 
        CHECK (status IN ('PENDENTE', 'CONTATADO', 'QUALIFICADO', 'DESCARTADO')),
    observacoes TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabela de INTERAÇÕES (Histórico e Auditoria)
CREATE TABLE interacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    consultor_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('LIGACAO', 'EMAIL', 'REUNIAO', 'OUTRO')),
    descricao TEXT NOT NULL,
    data_interacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);