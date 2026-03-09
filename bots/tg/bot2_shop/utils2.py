#корзина для отправки
def format_cart(cart):
    if not cart:
        return ""

    lines = []
    for i, item in enumerate(cart, 1):
        lines.append(f"{i}. {item['name']} - {item['price']}₽")

    return "\n".join(lines)

#счет прайса
def calculate_total(cart):
    return sum(item.get('price', 0) for item in cart)

#серч по айди продукта
def get_product_by_id(product_id):
    from .config2 import PRODUCTS
    return next((p for p in PRODUCTS if p["id"] == product_id), None)

#серч по айди каты
def get_category_by_id(category_id):
    from .config2 import CATEGORIES
    return next((c for c in CATEGORIES if c["id"] == category_id), None)