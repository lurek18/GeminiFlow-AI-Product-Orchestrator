import os
import logging

class GeminiAgent:
    def __init__(self):
        self.model_name = "gemini-2.0-flash"
        # Ceny za 1000 tokenů dle v3.0.4
        self.price_input = 0.00025
        self.price_output = 0.001

    def calculate_cost(self, prompt_tokens, completion_tokens):
        """Vypočítá přesnou cenu za volání AI."""
        cost = (prompt_tokens / 1000 * self.price_input) + (completion_tokens / 1000 * self.price_output)
        return round(cost, 5)

    def get_prompt_instructions(self):
        """Prompting Policy dle standardu."""
        return (
            "Jsi e-commerce specialista. Výstup generuj v češtině. "
            "Struktura: 1. Úvod (2 věty), 2. Tabulka parametrů (Markdown), "
            "3. Prodejní argumenty (odrážky), 4. SEO Meta Title a Description."
        )

    async def generate_content_async(self, name, description):
        """Simulace asynchronního volání Gemini API."""
        # Zde by byla reálná integrace s google.generativeai
        return {
            "content": f"Transformovaný obsah pro {name}",
            "cost": 0.00125  # Příklad vypočtené ceny
        }