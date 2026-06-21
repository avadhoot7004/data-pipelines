import psycopg2 
import psycopg2.extras 
from datetime import date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()  # load variables from .env file into environment

def run_incremental_etl(): 
    conn = psycopg2.connect( 
        host='host.docker.internal', # use this to connect from Airflow container to local Postgres on host machine
        port=5432, 
        dbname='postgres', 
        user='postgres', 
        password= ''  # read from .env 
    ) 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
 
    # WATERMARK logic
    # Find the latest order_date already loaded into the target 
    cursor.execute('SELECT MAX(order_date) FROM analytics_db.sales_summary') 
    result = cursor.fetchone()[0] 
    watermark = result if result else date(2000, 1, 1)  # default if table is empty 
    print(f'Watermark: {watermark} — loading orders after this date') 

    # watermark logic with lookback period (e.g., 7 days) 
    lookback_date = watermark - timedelta(days=7)
 
    # Extract new orders from source that are after the watermark and have status 'completed'
    cursor.execute( 
        ''' 
        SELECT * FROM orders_db.orders 
        WHERE status = %s 
          AND order_date > %s 
        ''', 
        ('completed', lookback_date) 
    ) 

    # ('completed', watermark) is replaced with ('completed', lookback_date) to include a lookback period of 7 days for reprocessing recent orders

    orders = cursor.fetchall() 
    print(f'Extracted {len(orders)} new orders from source') 
 
    cursor.execute('SELECT * FROM products_db.products') 
    products = {row['product_id']: row for row in cursor.fetchall()}
 
    # Transform: calculate total_amount and order_month, and prepare data for loading
    transformed = [] 
    skipped = 0 
    for order in orders: 
        product = products.get(order['product_id']) 
        if not product: 
            skipped += 1 
            continue 
        total_amount = order['quantity'] * product['unit_price'] 
        order_month  = order['order_date'].strftime('%Y-%m') 
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
 
    # Load: insert transformed data into target (analytics_db.sales_summary), using ON CONFLICT to avoid duplicates based on order_id 
    if transformed: 
        cursor.executemany( 
            ''' 
            INSERT INTO analytics_db.sales_summary 
                (order_id, customer_name, product_name, category, 
                 quantity, unit_price, total_amount, 
                 order_date, order_month, status) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            ON CONFLICT (order_id) 
            DO NOTHING 
            ''', 
            transformed 
        ) 
        conn.commit() 
    
    print(f'Loaded : {len(transformed)} rows') 
    print(f'Skipped: {skipped} rows (no matching product)') 
    cursor.close() 
    conn.close() 

def log_row_count():

    conn = psycopg2.connect(
        host='host.docker.internal',
        port=5432,
        dbname='postgres',
        user='postgres',
        password=''
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM analytics_db.sales_summary
    """)

    count = cursor.fetchone()[0]

    print(f"Current sales_summary row count: {count}")
    
    cursor.close()
    conn.close()
 
if __name__ == '__main__': 
    run_incremental_etl()