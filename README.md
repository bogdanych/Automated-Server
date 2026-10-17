# Итоговый проект: автоматизация обработки выгрузок касс

Проект эмулирует работу торговой сети: генерирует CSV-выгрузки из касс,
загружает их в базу данных и автоматизирует оба процесса через `cron`.

## Требования

- Python 3.9+
- PostgreSQL 14+
- cron (Linux Mint / Ubuntu / Debian)

Python-зависимости (`requirements.txt`):

```
psycopg2-binary==2.9.9
```

## Запуск на новой машине

### 1. Клонировать репозиторий

```bash
git clone <URL_репозитория>
cd project
```

### 2. Создать виртуальное окружение и поставить зависимости

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настроить PostgreSQL

Создать базу и пользователя:

```bash
sudo -u postgres psql
```

Внутри psql выполнить:

```sql
CREATE DATABASE retail;
CREATE USER retail_user WITH PASSWORD 'retail_pass';
GRANT ALL PRIVILEGES ON DATABASE retail TO retail_user;
\q
```

Для PostgreSQL 15+ выдать права на схему public:

```bash
sudo -u postgres psql -d retail -c "GRANT ALL ON SCHEMA public TO retail_user;"
```

Применить DDL (создать таблицы):

```bash
psql -h localhost -U retail_user -d retail -f sql/schema.sql
```

Пароль: `retail_pass`.

### 4. Проверить настройки

Открыть `config.py` и при необходимости изменить параметры:

```python
N_SHOPS = 5                # Количество магазинов
MAX_CASH_PER_SHOP = 5      # Максимум касс в магазине

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "retail"
DB_USER = "retail_user"
DB_PASSWORD = "retail_pass"
```

### 5. Ручной запуск

Сгенерировать CSV в `data/`:

```bash
python generate_data.py
```

Загрузить CSV в БД (после загрузки файлы переедут в `data/processed/`):

```bash
python load_data.py
```

Проверить, что данные попали в БД:

```bash
psql -h localhost -U retail_user -d retail -c "SELECT COUNT(*) FROM sales;"
```

### 6. Автоматизация через cron

Открыть crontab:

```bash
crontab -e
```

Добавить две строки (заменить `<PROJECT_PATH>` на абсолютный путь к папке проекта,
например `/home/user/project`):

```cron
# Генерация каждый день кроме воскресенья в 01:00
0 1 * * 1-6 <PROJECT_PATH>/venv/bin/python <PROJECT_PATH>/generate_data.py >> <PROJECT_PATH>/generate.log 2>&1

# Загрузка в БД каждый день в 02:00
0 2 * * * <PROJECT_PATH>/venv/bin/python <PROJECT_PATH>/load_data.py >> <PROJECT_PATH>/load.log 2>&1
```

Проверить, что задания сохранились:

```bash
crontab -l
```

Проверить логи после первого срабатывания:

```bash
tail -20 generate.log
tail -20 load.log
```

## Структура проекта

```
project/
├── config.py              # Настройки БД и параметров генерации
├── generate_data.py       # Генерация CSV в data/
├── load_data.py           # Загрузка CSV в БД
├── requirements.txt       # Зависимости Python
├── sql/schema.sql         # DDL-команды создания таблиц
├── data/                  # Примеры сгенерированных выгрузок
├── data/processed/        # Обработанные файлы
└── img/                   # Скриншоты cron и БД
```
