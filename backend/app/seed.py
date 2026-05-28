from sqlmodel import Session, select

from app.database import engine, init_db
from app.models import CodingTask, PipelineStatus


TASKS = [
    CodingTask(
        title="FizzBuzz Implementation",
        slug="fizzbuzz",
        category="api-coding",
        difficulty="easy",
        status=PipelineStatus.experiment,
        prompt="""Implement a function fizzbuzz(n: int) -> list[str].

Rules:
- Multiples of 3 return "Fizz"
- Multiples of 5 return "Buzz"
- Multiples of both return "FizzBuzz"
- Other numbers return the number as a string
- Return results from 1 through n inclusive
""",
        starter_code="""def fizzbuzz(n: int) -> list[str]:
    # TODO: implement
    pass
""",
        tests_code="""from solution import fizzbuzz

def test_fizzbuzz_15():
    assert fizzbuzz(15) == [
        "1", "2", "Fizz", "4", "Buzz",
        "Fizz", "7", "8", "Fizz", "Buzz",
        "11", "Fizz", "13", "14", "FizzBuzz"
    ]

def test_fizzbuzz_1():
    assert fizzbuzz(1) == ["1"]
""",
    ),
    CodingTask(
        title="Bugfix Shopping Cart Total",
        slug="bugfix-cart-total",
        category="bugfix",
        difficulty="medium",
        status=PipelineStatus.idea,
        prompt="""Fix the cart_total function.

It should:
- Multiply price by quantity
- Apply discount_percent to the subtotal
- Return a rounded float with 2 decimal places
- Ignore items with quantity 0

Input example:
[
    {"price": 10.0, "quantity": 2},
    {"price": 5.0, "quantity": 1}
]
""",
        starter_code="""def cart_total(items: list[dict], discount_percent: float = 0) -> float:
    total = 0
    for item in items:
        total += item["price"]
    total = total - discount_percent
    return total
""",
        tests_code="""from solution import cart_total

def test_cart_total_without_discount():
    items = [
        {"price": 10.0, "quantity": 2},
        {"price": 5.0, "quantity": 1},
    ]
    assert cart_total(items) == 25.00

def test_cart_total_with_discount():
    items = [
        {"price": 100.0, "quantity": 1},
        {"price": 50.0, "quantity": 2},
    ]
    assert cart_total(items, discount_percent=10) == 180.00

def test_cart_total_ignores_zero_quantity():
    items = [
        {"price": 100.0, "quantity": 0},
        {"price": 20.0, "quantity": 2},
    ]
    assert cart_total(items) == 40.00
""",
    ),
]


def seed():
    init_db()
    with Session(engine) as session:
        existing = session.exec(select(CodingTask)).all()
        if existing:
            print("Database already seeded.")
            return

        for task in TASKS:
            session.add(task)

        session.commit()
        print("Seeded sample coding tasks.")


if __name__ == "__main__":
    seed()
