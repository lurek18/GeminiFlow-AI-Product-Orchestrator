import os
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, quality=80):
        self.quality = quality # Standard dle v3.0.4

    def process_for_seo(self, image_path, product_name, sku):
        """
        Konverze do WebP a SEO přejmenování dle protokolu.
        Vzor: [nazev-produktu]-xml-conv-[sku].webp
        """
        try:
            # Vyčištění názvu pro URL/File standard
            clean_name = product_name.lower().replace(" ", "-").replace("/", "-")
            new_filename = f"{clean_name}-xml-conv-{sku}.webp"
            output_path = os.path.join("data", new_filename)

            # Realizace konverze přes Pillow
            with Image.open(image_path) as img:
                img.save(output_path, "WEBP", quality=self.quality)
            
            logger.info(f"📸 Obrázek optimalizován: {new_filename}")
            return output_path
        except Exception as e:
            logger.error(f"❌ Chyba při zpracování obrázku {sku}: {str(e)}")
            return None