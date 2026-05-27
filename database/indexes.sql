CREATE INDEX IF NOT EXISTS idx_empresas_cnae ON empresas(cnae_principal);
CREATE INDEX IF NOT EXISTS idx_empresas_capital ON empresas(capital_social);
CREATE INDEX IF NOT EXISTS idx_empresas_localizacao ON empresas(uf, municipio);
CREATE INDEX IF NOT EXISTS idx_empresas_situacao ON empresas(situacao);
CREATE INDEX IF NOT EXISTS idx_leads_consultor_status ON leads(consultor_id, status);
CREATE INDEX IF NOT EXISTS idx_interacoes_lead_data ON interacoes(lead_id, data_interacao DESC);
CREATE INDEX IF NOT EXISTS idx_password_reset_token ON password_reset_tokens(token);
CREATE INDEX IF NOT EXISTS idx_refresh_token ON refresh_tokens(token);
