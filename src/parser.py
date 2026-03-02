import xml.etree.ElementTree as ET

def parse_external_feed(file_path):
    """Parsování vstupního XML feedu."""
    products = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for item in root.findall('.//SHOPITEM'):
            products.append({
                "sku": item.find('SKU').text,
                "name": item.find('PRODUCTNAME').text,
                "description": item.find('DESCRIPTION').text,
                "params": {} # Zde by byla logika pro parametry
            })
    except Exception:
        # Pro showcase vracíme dummy data, pokud soubor chybí
        products = [{"sku": "SH-01", "name": "Test Produkt", "description": "Popis", "params": {}}]
    return products