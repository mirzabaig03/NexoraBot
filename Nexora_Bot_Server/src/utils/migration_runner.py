import os
import psycopg2
from pathlib import Path


def run_migrations():
    print("Running database migrations...")

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn.autocommit = True

    cursor = conn.cursor()

    migrations_path = Path("supabase/migrations")

    for file in sorted(migrations_path.glob("*.sql")):
        print(f"Applying migration: {file.name}")

        sql = file.read_text()

        try:
            cursor.execute(sql)
        except Exception as e:
            print(f"Migration skipped: {e}")

    cursor.close()
    conn.close()