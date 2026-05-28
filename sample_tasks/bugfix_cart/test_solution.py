from solution import cart_total

def test_cart_total():
    assert cart_total([{"price": 10, "quantity": 2}]) == 20
