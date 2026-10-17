import csv
import os
import re
import shutil
from datetime import datetime
import psycopg2  # или sqlite3, если используете SQLite
import config

FILENAME_RE = re.compile(r"^(\d+)_(\d+)\.csv$")

def get_db_connection():
    """Возвращает соединение с PostgreSQL."""
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
    )

def load_file(conn, filepath: str, shop_num: int, cash_num: int):
    """Загружает один csv в БД. Возвращает количество вставленных строк."""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append((
                row["doc_id"],
                row["item"],
                row["category"],
                int(row["amount"]),
                float(row["price"]),
                float(row["discount"]),
                shop_num,
                cash_num,
            ))
    if not rows:
        return 0
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO sales
                (doc_id, item, category, amount, price, discount, shop_num, cash_num)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )
    conn.commit()
    return len(rows)

def main():
    os.makedirs(config.PROCESSED_DIR, exist_ok=True)
    conn = get_db_connection()
    total_loaded = 0
    try:
        for filename in os.listdir(config.DATA_DIR):
            filepath = os.path.join(config.DATA_DIR, filename)
            if not os.path.isfile(filepath):
                continue
            match = FILENAME_RE.match(filename)
            if not match:
                print(f"[{datetime.now()}] Пропущен файл (не соответствует шаблону): {filename}")
                continue
            shop_num = int(match.group(1))
            cash_num = int(match.group(2))
            try:
                count = load_file(conn, filepath, shop_num, cash_num)
                total_loaded += count
                # Перемещаем обработанный файл в архив
                dest = os.path.join(config.PROCESSED_DIR, filename)
                # Если файл с таким именем уже есть, добавляем timestamp
                if os.path.exists(dest):
                    base, ext = os.path.splitext(filename)
                    dest = os.path.join(
                        config.PROCESSED_DIR,
                        f"{base}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
                    )
                shutil.move(filepath, dest)
                print(f"[{datetime.now()}] Загружен {filename}: {count} строк")
            except Exception as e:
                print(f"[{datetime.now()}] Ошибка при загрузке {filename}: {e}")
                conn.rollback()
    finally:
        conn.close()
    print(f"[{datetime.now()}] Всего загружено строк: {total_loaded}")

if __name__ == "__main__":
    main()