import asyncio
import logging
import sys
from src.ai_agent import GeminiAgent
from src.database.repository import SupabaseRepository

# --- KONFIGURACE ORCHESTRÁTORU (v3.0.4) ---

# Nastavení logování pro profesionální monitoring
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# OPRAVA: Sdílený semafor pro omezení paralelismu na max 10 úloh
semaphore = asyncio.Semaphore(10)

# Globální čítač pro Zákon Circuit Breakeru
consecutive_errors = 0
MAX_CONSECUTIVE_ERRORS = 10

async def process_product(product, repo, agent):
    """
    Zpracuje jeden produkt s implementací retry logiky, 
    backoffu a záchranného mechanismu.
    """
    global consecutive_errors
    sku = product.get('sku')
    retries = product.get('error_count', 0)
    MAX_RETRIES = 5  # Zákon Záchrany
    
    # Exponenciální časy čekání v minutách
    backoff_schedule = [1, 5, 15, 30, 60]

    async with semaphore: # Správné užití sdíleného limitu
        try:
            logger.info(f"⚙️ Zahajuji zpracování SKU: {sku} (Pokus {retries + 1}/{MAX_RETRIES})")
            
            # Simulace AI transformace přes Gemini 2.0 Flash
            # ai_result = await agent.generate_content_async(...)
            
            # Simulace úspěchu
            await asyncio.sleep(1) 
            
            # Reset čítače Circuit Breakeru při úspěchu
            consecutive_errors = 0
            
            # Aktualizace statusu na 'synced'
            # await repo.update_status(sku, 'synced', ai_result)
            logger.info(f"✅ SKU {sku} úspěšně synchronizováno.")
            
        except Exception as e:
            consecutive_errors += 1
            retries += 1
            
            # Kontrola Zákona Circuit Breakeru
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                logger.critical(f"🚨 CIRCUIT BREAKER AKTIVOVÁN: {MAX_CONSECUTIVE_ERRORS} chyb v řadě. Zastavuji systém!")
                sys.exit(1) # Okamžité zastavení systému

            # Kontrola Zákona Záchrany
            if retries >= MAX_RETRIES:
                logger.error(f"❌ SKU {sku} selhalo {MAX_RETRIES}x. Přesun do 'manual_review'.")
                # await repo.update_status(sku, 'manual_review')
            else:
                # Implementace Zákona Backoffu
                wait_min = backoff_schedule[min(retries - 1, len(backoff_schedule) - 1)]
                logger.warning(f"⚠️ Chyba u {sku}. Backoff: Čekám {wait_min} min před dalším pokusem.")
                # V produkci: await asyncio.sleep(wait_min * 60)

async def main():
    """Hlavní smyčka orchestrátoru."""
    repo = SupabaseRepository()
    agent = GeminiAgent()
    
    logger.info("🏁 Spouštím Wordpress XML convertor Orchestrator v3.0.4")
    
    # Načtení produktů ke zpracování (limit batchingu 100)
    # products = await repo.get_pending_products(limit=100)
    
    # Dummy data pro showcase
    mock_products = [{"sku": f"PROD-{i}", "error_count": 0} for i in range(25)]
    
    # Vytvoření asynchronních úloh
    tasks = [process_product(p, repo, agent) for p in mock_products]
    
    # Spuštění paralelního zpracování
    await asyncio.gather(*tasks)
    logger.info("✨ Všechny asynchronní úlohy byly dokončeny.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Orchestrátor ručně zastaven uživatelem.")