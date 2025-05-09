def calculate_cart_total(cart_entries, price_service):
    total = 0.0
    for entry in cart_entries:
        product_id = entry['product_id']
        quantity = entry['quantity']
        price = price_service.get_price(product_id)
        total += price * quantity
    return total

def validate_cart_entries(cart_entries):
    if not isinstance(cart_entries, list):
        raise ValueError("Cart entries must be a list.")
    for entry in cart_entries:
        if 'product_id' not in entry or 'quantity' not in entry:
            raise ValueError("Each cart entry must contain 'product_id' and 'quantity'.")
        if not isinstance(entry['quantity'], int) or entry['quantity'] <= 0:
            raise ValueError("Quantity must be a positive integer.")