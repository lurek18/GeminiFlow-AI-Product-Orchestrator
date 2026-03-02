# 🚀 Wordpress XML Convertor v3.0.4

Asynchronní mikro-služba pro transformaci XML feedů do WooCommerce pomocí AI Gemini 2.0 Flash.

## ✨ Klíčové funkce
- **AI Orchestrace:** Paralelní zpracování s limitem 10 úloh.
- **Cost Tracking:** Přesný výpočet nákladů na tokeny u každého produktu.
- **Circuit Breaker:** Automatické zastavení systému při 10 chybách v řadě.
- **Image SEO:** Konverze do WebP (80 % kvalita) a SEO naming standard.

## 🛠 Instalace
1. `pip install -r requirements.txt`
2. Nastavte `.env` podle `.env.example`
3. Spusťte `python sync_provider.py` pro import dat.
4. Spusťte `python main.py` pro AI transformaci.