import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "sample_store.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS products")

    # Customers
    cursor.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        country TEXT
    )
    """)

    # Products
    cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL
    )
    """)

    # Orders
    cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    # Order Items
    cursor.execute("""
    CREATE TABLE order_items (
        id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        sales_amount REAL,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    conn.commit()

    # Insert customers
    countries = ["USA", "UK", "Germany", "India", "Canada"]
    for i in range(1, 21):
        cursor.execute(
            "INSERT INTO customers VALUES (?, ?, ?, ?)",
            (
                i,
                f"Customer {i}",
                f"customer{i}@example.com",
                random.choice(countries),
            ),
        )

    # Insert products
    categories = ["Electronics", "Clothing", "Home", "Sports"]
    for i in range(1, 16):
        price = round(random.uniform(10, 500), 2)
        cursor.execute(
            "INSERT INTO products VALUES (?, ?, ?, ?)",
            (
                i,
                f"Product {i}",
                random.choice(categories),
                price,
            ),
        )

    # Insert orders
    start_date = datetime(2023, 1, 1)

    for i in range(1, 51):
        order_date = start_date + timedelta(days=random.randint(0, 365))
        cursor.execute(
            "INSERT INTO orders VALUES (?, ?, ?)",
            (
                i,
                random.randint(1, 20),
                order_date.strftime("%Y-%m-%d"),
            ),
        )

    # Insert order items
    for i in range(1, 200):
        order_id = random.randint(1, 50)
        product_id = random.randint(1, 15)
        quantity = random.randint(1, 5)
        price = cursor.execute(
            "SELECT price FROM products WHERE id=?", (product_id,)
        ).fetchone()[0]

        sales_amount = quantity * price

        cursor.execute(
            "INSERT INTO order_items VALUES (?, ?, ?, ?, ?)",
            (
                i,
                order_id,
                product_id,
                quantity,
                sales_amount,
            ),
        )

    conn.commit()
    conn.close()

    print(f"Database '{DB_NAME}' created successfully.")


if __name__ == "__main__":
    create_database()


#sqlite:////c:/Users/aadit/Desktop/projects/ai-analyst/sample_store.db