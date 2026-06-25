"""
Test CSV генерациялау:
python scripts/generate_sample_data.py
"""

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

PRODUCTS = {
    "Laptop": "Electronics",
    "Phone": "Electronics",
    "Tablet": "Electronics",
    "Chair": "Furniture",
    "Desk": "Furniture",
    "Monitor": "Electronics",
    "Keyboard": "Electronics",
    "Mouse": "Electronics",
    "Bookshelf": "Furniture",
    "Lamp": "Furniture",
}

REGIONS = ["North", "South", "East", "West", "Central"]


def generate(n_rows: int = 500) -> pd.DataFrame:
    rows = []
    start = date(2023, 1, 1)

    for _ in range(n_rows):
        product = random.choice(list(PRODUCTS.keys()))
        category = PRODUCTS[product]
        region = random.choice(REGIONS)
        quantity = random.randint(1, 10)
        unit_price = random.uniform(50, 2000)
        sales = round(quantity * unit_price, 2)
        profit = round(sales * random.uniform(0.05, 0.35), 2)
        order_date = start + timedelta(days=random.randint(0, 730))

        rows.append(
            {
                "order_date": order_date.strftime("%Y-%m-%d"),
                "product": product,
                "category": category,
                "region": region,
                "quantity": quantity,
                "sales": sales,
                "profit": profit,
            }
        )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    output = Path("data/raw/sales.csv")
    output.parent.mkdir(parents=True, exist_ok=True)

    df = generate(500)
    df.to_csv(output, index=False)

    print(f"[OK] Generated {len(df)} rows -> {output}")
    print(df.head())
