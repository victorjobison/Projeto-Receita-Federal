-- Acelera o filtro principal: Buscar empresas ativas por CNAE e Capital Social
CREATE INDEX idx_empresas_filtro_prospeccao 
ON empresas(cnae_principal, capital_social) 
WHERE status_rfb = 'ATIVA';

-- Acelera o carregamento do painel da consultora (buscar leads de um usuário específico)
CREATE INDEX idx_leads_painel_consultor 
ON leads(consultor_id, status);

-- Acelera o carregamento do histórico de um lead específico
CREATE INDEX idx_interacoes_lead 
ON interacoes(lead_id);