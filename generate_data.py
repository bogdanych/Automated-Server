import csv
import os
import random
import uuid
from datetime import datetime
import config

# Справочник товаров
CATEGORIES = {
    "Бытовая химия": [
        "Стиральный порошок", "Мыло", "Шампунь", "Средство для мытья посуды",
        "Чистящее средство", "Кондиционер для белья"
    ],
    "Текстиль": [
        "Полотенце", "Простыня", "Наволочка", "Плед", "Скатерть"
    ],
    "Посуда": [
        "Тарелка", "Чашка", "Ложка", "Вилка", "Кастрюля", "Сковорода"
    ]
}

def generate_check_rows(shop_num: int, cash_num: int):
    """Генерирует список строк для одного чека."""
    doc_id = uuid.uuid4().hex  # численно-буквенный идентификатор
    rows_count = random.randint(config.ROWS_PER_CHECK_MIN, config.ROWS_PER_CHECK_MAX)
    rows = []
    for _ in range(rows_count):
        category = random.choice(list(CATEGORIES.keys()))
        item = random.choice(CATEGORIES[category])
        amount = random.randint(1, 10)
        price = round(random.uniform(50, 2000), 2)
        # Скидка 0 или случайная до 50% от стоимости позиции
        if random.random() < 0.3:
            discount = round(price * amount * random.uniform(0.05, 0.5), 2)
        else:
            discount = 0.0
        rows.append({
            "doc_id": doc_id,
            "item": item,
            "category": category,
            "amount": amount,
            "price": price,
            "discount": discount,
        })
    return rows

def generate_for_cash(shop_num: int, cash_num: int, date_str: str):
    """Создаёт csv-файл для одной кассы."""
    filename = f"{shop_num}_{cash_num}.csv"
    filepath = os.path.join(config.DATA_DIR, filename)
    # Для эмуляции дневной выгрузки генерируем 10-30 чеков
    checks_count = random.randint(10, 30)
    all_rows = []
    for _ in range(checks_count):
        all_rows.extend(generate_check_rows(shop_num, cash_num))

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["doc_id", "item", "category", "amount", "price", "discount"]
        )
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"[{datetime.now()}] Сгенерирован файл: {filename} ({len(all_rows)} строк)")

def main():
    os.makedirs(config.DATA_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    for shop in range(1, config.N_SHOPS + 1):
        cash_count = random.randint(1, config.MAX_CASH_PER_SHOP)
        for cash in range(1, cash_count + 1):
            generate_for_cash(shop, cash, date_str)

if __name__ == "__main__":
    main()