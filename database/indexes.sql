-- 1. Acelera filtros por CNAE principal na busca de empresas.
CREATE INDEX IF NOT EXISTS idx_empresas_cnae ON empresas(cnae_principal);

-- 2. Acelera ordenacao/filtro por capital social.
CREATE INDEX IF NOT EXISTS idx_empresas_capital ON empresas(capital_social);

-- 3. Acelera filtros combinados por UF e municipio.
CREATE INDEX IF NOT EXISTS idx_empresas_localizacao ON empresas(uf, municipio);

-- 4. Acelera filtro por situacao cadastral.
CREATE INDEX IF NOT EXISTS idx_empresas_situacao ON empresas(situacao);

-- 5. Acelera a listagem do funil por consultor e status.
CREATE INDEX IF NOT EXISTS idx_leads_consultor_status ON leads(consultor_id, status);

-- 6. Acelera o historico de interacoes por lead em ordem cronologica.
CREATE INDEX IF NOT EXISTS idx_interacoes_lead_data ON interacoes(lead_id, data_interacao DESC);

-- 7. Acelera validacao de token de recuperacao de senha.
CREATE INDEX IF NOT EXISTS idx_password_reset_token ON password_reset_tokens(token);

-- 8. Acelera validacao e revogacao de refresh token.
CREATE INDEX IF NOT EXISTS idx_refresh_token ON refresh_tokens(token);
