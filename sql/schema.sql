-- Для PostgreSQL
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    doc_id VARCHAR(50) NOT NULL,
    item VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    amount INTEGER NOT NULL CHECK (amount > 0),
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    discount NUMERIC(10, 2) DEFAULT 0 CHECK (discount >= 0),
    shop_num INTEGER NOT NULL,
    cash_num INTEGER NOT NULL,
    sale_date DATE DEFAULT CURRENT_DATE,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sales_doc_id ON sales(doc_id);
CREATE INDEX IF NOT EXISTS idx_sales_shop_cash ON sales(shop_num, cash_num);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);