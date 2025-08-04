import pandas as pd
import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# DROP old users table just to be safe (optional but recommended)
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("DROP TABLE IF EXISTS orders;")

# Create users table (correct structure)
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    age INTEGER,
    gender TEXT,
    state TEXT,
    street_address TEXT,
    postal_code TEXT,
    city TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL,
    traffic_source TEXT,
    created_at TEXT
);
''')

# Create orders table
# Create orders table (matching CSV)
cursor.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    status TEXT,
    gender TEXT,
    created_at TEXT,
    returned_at TEXT,
    shipped_at TEXT,
    delivered_at TEXT,
    num_of_item INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')


# Load CSVs
users_df = pd.read_csv('users.csv')
orders_df = pd.read_csv('orders.csv')

# Optional: print columns to verify
print("users.csv columns:", users_df.columns.tolist())
print("orders.csv columns:", orders_df.columns.tolist())

# Insert data
users_df.to_sql('users', conn, if_exists='append', index=False)
orders_df.to_sql('orders', conn, if_exists='append', index=False)

# Check data
print("\nUsers Table Sample:")
print(pd.read_sql_query("SELECT * FROM users LIMIT 5;", conn))

print("\nOrders Table Sample:")
print(pd.read_sql_query("SELECT * FROM orders LIMIT 5;", conn))

# Row count
print("\nUsers Row Count:")
print(pd.read_sql_query("SELECT COUNT(*) FROM users;", conn))

print("\nOrders Row Count:")
print(pd.read_sql_query("SELECT COUNT(*) FROM orders;", conn))

# Done
conn.close()
