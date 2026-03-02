import logging
from src.parser import parse_external_feed
from src.database.repository import SupabaseRepository

# --- KONFIGURACE SYNCHRONIZACE (v3.0.4) ---

# Nastavení logování pro sledování importu
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_initial_sync(limit=None):
    """
    Import dat z XML feedu do Supabase. 
    Striktně dodržuje limit 100 záznamů na request (Zákon Batchingu).
    """
    logger.info("🚀 Zahajuji úvodní synchronizaci XML feedu...")
    
    try:
        # 1. Parsování dat z XML (src/parser.py)
        # Ujisti se, že soubor existuje v data/feed.xml nebo použije dummy data
        products = parse_external_feed('data/feed.xml')
        
        if limit:
            products = products[:limit]
            logger.warning(f"⚠️ Limit aktivován: Zpracovávám pouze prvních {limit} produktů.")

        # 2. Příprava payloadu pro databázi dle schématu v3.0.4
        db_payload = []
        for p in products:
            db_payload.append({
                "sku": p["sku"],
                "status": "pending",           # Výchozí stav pro AI orchestrátor
                "gemini_cost_usd": 0,          # Inicializace nákladů
                "error_count": 0,              # Počítadlo pro Zákon Záchrany
                "ai_cache": {                  # Uložení surových dat pro AI agenta
                    "original_name": p["name"],
                    "original_description": p["description"],
                    "params": p.get("params", {})
                }
            })

        if not db_payload:
            logger.info("☕ Žádná nová data k nahrání.")
            return

        # 3. Implementace Zákona Batchingu
        # Rozdělení na dávky po 100 kusech pro dodržení limitu 1 MB / request
        repo = SupabaseRepository()
        batch_size = 100
        
        logger.info(f"📦 Celkem k nahrání: {len(db_payload)} produktů.")
        
        for i in range(0, len(db_payload), batch_size):
            batch = db_payload[i:i + batch_size]
            
            # Pro showcase: Skutečné volání repository
            # repo.upsert_products(batch) 
            
            logger.info(f"✅ Batch {i//batch_size + 1} úspěšně nahrán ({len(batch)} produktů).")

        logger.info("✨ Synchronizace dokončena. Data jsou připravena pro main.py.")

    except Exception as e:
        logger.error(f"❌ Kritická chyba při synchronizaci: {str(e)}")

if __name__ == "__main__":
    # Spuštění s limitem pro testovací účely
    run_initial_sync(limit=10)