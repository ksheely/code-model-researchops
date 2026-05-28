def cart_total(items: list[dict], discount_percent: float = 0) -> float:
    subtotal = sum(
        item["price"] * item["quantity"]
        for item in items
        if item["quantity"] > 0
    )
    discounted = subtotal * (1 - discount_percent / 100)
    return round(discounted, 2)
