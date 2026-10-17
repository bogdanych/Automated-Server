import os

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# Параметры генерации
N_SHOPS = 5                # количество магазинов
MAX_CASH_PER_SHOP = 5      # максимальное число касс в магазине
ROWS_PER_CHECK_MIN = 1
ROWS_PER_CHECK_MAX = 5

# Подключение к PostgreSQL
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "retail"
DB_USER = "retail_user"
DB_PASSWORD = "retail_pass"

