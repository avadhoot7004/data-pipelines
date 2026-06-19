from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://uid:pass@localhost:5432/adventureworks"
)

with engine.connect() as conn:
    print("Connected to PostgreSQL!")