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

print(f"Orders extracted: {len(orders)}")
print(f"Products extracted: {len(products)}")

# --- TRANSFORM ---

transformed = []
skipped_rows = 0

for order in orders:
    product = products.get(order['product_id'])
    if not product:
        skipped_rows += 1 #for every skipped row
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

cursor.executemany(
    """
    INSERT INTO analytics_db.sales_summary
    (
        order_id,
        customer_name,
        product_name,
        category,
        quantity,
        unit_price,
        total_amount,
        order_date,
        order_month,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (order_id)   
    DO NOTHING
    """,
    transformed
)

#added ON CONFLICT clause to avoid duplicate entries if the script is run multiple times

# CUSTOMER AGGREGATION

cursor.execute("""
    SELECT customer_name, total_amount
    FROM analytics_db.sales_summary
""")

sales = cursor.fetchall()

customer_totals = {}

for row in sales:
    customer = row['customer_name']
    amount = float(row['total_amount'])

    if customer not in customer_totals:
        customer_totals[customer] = {
            'total_spend': 0,
            'order_count': 0
        }

    customer_totals[customer]['total_spend'] += amount
    customer_totals[customer]['order_count'] += 1

aggregated_rows = []

for customer, data in customer_totals.items():
    aggregated_rows.append((
        customer,
        round(data['total_spend'], 2),
        data['order_count']
    ))

cursor.execute("TRUNCATE TABLE analytics_db.customer_totals") #entries get dropped for every run of the script to avoid duplicates

cursor.executemany(
    """
    INSERT INTO analytics_db.customer_totals
    (
        customer_name,
        total_spend,
        order_count
    )
    VALUES (%s, %s, %s)
    """,
    aggregated_rows
)


conn.commit()

#print(f'Loaded {len(transformed)} records into analytics_db.sales_summary')

# LOGGING

print("\n--------- ETL SUMMARY ----------")
print(f"Orders extracted : {len(orders)}")
print(f"Products extracted : {len(products)}")
print(f"Rows skipped : {skipped_rows}")
print(f"Customer totals generated for {len(aggregated_rows)} customers")
print(f"Loaded : {len(transformed)} rows in analytics_db.sales_summary")
print("------------------------------------")

cursor.close()
conn.close()