import psycopg2
import psycopg2.extras


conn = psycopg2.connect(
 host='localhost', port=5432,
 dbname='postgres',
 user='postgres', password='1234'
)

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# --- EXTRACT ---

cursor.execute("SELECT * FROM orders_db.orders WHERE status = 'completed'")

orders = cursor.fetchall()

cursor.execute('SELECT * FROM products_db.products')

products = {row['product_id']: row for row in cursor.fetchall()}

# --- TRANSFORM ---

transformed = []

for order in orders:
    product = products.get(order['product_id'])
    if not product:
        continue # skip if no matching product
    total_amount = order['quantity'] * product['unit_price']
    order_month = order['order_date'].strftime('%Y-%m')
    transformed.append((
        order['order_id'],
        order['customer_name'],
        product['product_name'],
        product['category'],
        order['quantity'],
        product['unit_price'],
        total_amount,
        order['order_date'],
        order_month,
        order['status']
    ))

# --- LOAD ---

# TODO: Write an INSERT INTO analytics_db.sales_summary statement
# TODO: Use cursor.executemany() to insert all rows in 'transformed'
# TODO: Call conn.commit() to save the changes


conn.commit()

cursor.close()

conn.close()

print(f'Loaded {len(transformed)} records into analytics_db.sales_summary')