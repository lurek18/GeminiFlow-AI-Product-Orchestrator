-- ==========================================
-- PROJECT: Wordpress XML Convertor (v3.0.4)
-- DESCRIPTION: Database Schema for Supabase
-- ==========================================

-- 1. Definice stavů synchronizace (Dle protokolu v3.0.4)
-- Povoluje sledování životního cyklu produktu od importu po finální sync
DO $$ BEGIN
    CREATE TYPE sync_status AS ENUM (
        'pending',          -- Čeká na AI zpracování
        'processing',       -- Právě se generuje obsah
        'synced',           -- Úspěšně nahráno do e-shopu
        'error',            -- Došlo k chybě (vstoupí do retry logiky)
        'manual_review'     -- Selhalo 5x, vyžaduje lidský zásah
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Hlavní tabulka produktů
-- Navrženo pro batching 100 záznamů a sledování nákladů na Gemini
CREATE TABLE IF NOT EXISTS products_sync (
    sku VARCHAR(255) PRIMARY KEY,                   -- Unikátní identifikátor produktu
    status sync_status DEFAULT 'pending',           -- Aktuální stav v pipeline
    ai_cache JSONB DEFAULT '{}'::jsonb,             -- Metadata: {original_name, description, params, generated_content}
    gemini_cost_usd NUMERIC(10, 5) DEFAULT 0,       -- Přesné náklady na AI transformaci
    error_count INTEGER DEFAULT 0,                  -- Počítadlo selhání pro Circuit Breaker
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Monitoring Dashboard (SQL View)
-- OPRAVENO: Název sjednocen s dokumentací z 'sync_summary' na 'sync_dashboard'
CREATE OR REPLACE VIEW sync_dashboard AS
SELECT 
    status, 
    COUNT(*) as total_count, 
    SUM(gemini_cost_usd) as total_spent_usd,
    MAX(updated_at) as last_update
FROM products_sync 
GROUP BY status;

-- Index pro rychlé vyhledávání produktů ke zpracování orchestrátorem
CREATE INDEX IF NOT EXISTS idx_products_pending ON products_sync(status) WHERE status = 'pending';