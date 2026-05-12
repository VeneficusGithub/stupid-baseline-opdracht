import csv
import os
import random
from datetime import datetime, timedelta

from faker import Faker

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw_returns.csv")
ROW_COUNT = 100_000

PRODUCT_CATEGORIES = [
    "Road",
    "Mountain",
    "City",
    "E-Bike",
    "Gravel",
    "Kids",
    "Folding",
    "Touring",
]

SHIFT_TYPES = ["Day", "Evening", "Night", "Weekend"]
LOCATIONS = [
    "Amsterdam",
    "Rotterdam",
    "Utrecht",
    "Eindhoven",
]

HIDDEN_NA_VALUES = ["null", "N/A", " "]


def generate_order_date(fake: Faker) -> str:
    order_date = fake.date_between(start_date="-2y", end_date="today")
    if random.random() < 0.20:
        return order_date.strftime("%d/%m/%Y")
    return order_date.isoformat()


def generate_price() -> str:
    price_value = round(random.uniform(299.00, 3499.99), 2)
    if random.random() < 0.30:
        euros = int(price_value)
        cents = int(round((price_value - euros) * 100))
        return f"€{euros},{cents:02d}"
    return f"{price_value:.2f}"


def maybe_inject_hidden_na(value: str) -> str:
    if random.random() < 0.10:
        return random.choice(HIDDEN_NA_VALUES)
    return value


def get_defect_probability(shift_type: str, location: str) -> float:
    if shift_type == "Night" and location == "Amsterdam":
        return 0.3
    if shift_type == "Night":
        return 0.15
    if location == "Amsterdam":
        return 0.15
    return 0.05


def assemble_row(fake: Faker) -> dict:
    order_id = fake.uuid4()
    customer_id = fake.uuid4()
    customer_name = fake.name()
    product_id = fake.uuid4()
    product_category = random.choice(PRODUCT_CATEGORIES)
    shift_type = random.choice(SHIFT_TYPES)
    location = random.choice(LOCATIONS)
    order_date = generate_order_date(fake)
    price = generate_price()

    base_defect_probability = get_defect_probability(shift_type, location)
    is_defect = 1 if random.random() < base_defect_probability else 0

    # Inject hidden NaN values into categorical features after defect logic is determined.
    if random.random() < 0.10:
        product_category = random.choice(HIDDEN_NA_VALUES)
    if random.random() < 0.10:
        shift_type = random.choice(HIDDEN_NA_VALUES)
    if random.random() < 0.10:
        location = random.choice(HIDDEN_NA_VALUES)

    return {
        "order_id": order_id,
        "customer_id": customer_id,
        "customer_name": customer_name,
        "product_id": product_id,
        "product_category": product_category,
        "shift_type": shift_type,
        "location": location,
        "order_date": order_date,
        "price": price,
        "is_defect": is_defect,
    }


def write_data():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    fake = Faker("nl_NL")
    Faker.seed(42)
    random.seed(12)

    fieldnames = [
        "order_id",
        "customer_id",
        "customer_name",
        "product_id",
        "product_category",
        "shift_type",
        "location",
        "order_date",
        "price",
        "is_defect",
    ]

    rows = []
    defect_indices = []

    for row_index in range(ROW_COUNT):
        row = assemble_row(fake)
        rows.append(row)
        if row["is_defect"] == 1:
            defect_indices.append(row_index)

    blank_count = int(len(defect_indices) * 0.40)
    blanks_to_apply = set(random.sample(defect_indices, blank_count)) if blank_count > 0 else set()
    for row_index in blanks_to_apply:
        rows[row_index]["is_defect"] = ""

    with open(OUTPUT_PATH, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    write_data()
    print(f"Generated {ROW_COUNT} rows at {OUTPUT_PATH}")
