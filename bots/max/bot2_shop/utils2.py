from config2 import PRODUCTS, CATEGORIES

def get_product_by_id(product_id):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)

def get_category_by_id(category_id):
    return next((c for c in CATEGORIES if c["id"] == category_id), None)

def format_cart(cart):
    if not cart:
        return ""
    lines = []
    for i, item in enumerate(cart, 1):
        lines.append(f"{i}. {item['name']} - {item['price']}₽")
    return "\n".join(lines)

def calculate_total(cart):
    return sum(item.get('price', 0) for item in cart)