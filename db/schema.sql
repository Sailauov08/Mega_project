-- Sales Forecast Pipeline — Database Schema

CREATE TABLE IF NOT EXISTS raw_sales (
    id          SERIAL PRIMARY KEY,
    order_date  DATE,
    product     VARCHAR(200),
    category    VARCHAR(100),
    region      VARCHAR(100),
    quantity    INTEGER,
    sales       NUMERIC(12, 2),
    profit      NUMERIC(12, 2),
    loaded_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS clean_sales (
    id          SERIAL PRIMARY KEY,
    order_date  DATE         NOT NULL,
    product     VARCHAR(200) NOT NULL,
    category    VARCHAR(100) NOT NULL,
    region      VARCHAR(100) NOT NULL,
    quantity    INTEGER      NOT NULL CHECK (quantity > 0),
    sales       NUMERIC(12, 2) NOT NULL CHECK (sales >= 0),
    profit      NUMERIC(12, 2),
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS daily_metrics (
    id              SERIAL PRIMARY KEY,
    metric_date     DATE            NOT NULL UNIQUE,
    total_sales     NUMERIC(14, 2)  NOT NULL,
    total_profit    NUMERIC(14, 2),
    total_quantity  INTEGER         NOT NULL,
    order_count     INTEGER         NOT NULL,
    avg_order_value NUMERIC(12, 2),
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS predictions (
    id              SERIAL PRIMARY KEY,
    predict_date    DATE            NOT NULL,
    predicted_sales NUMERIC(14, 2)  NOT NULL,
    actual_sales    NUMERIC(14, 2),
    model_version   VARCHAR(50)     DEFAULT 'v1',
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pipeline_logs (
    id          SERIAL PRIMARY KEY,
    step        VARCHAR(100) NOT NULL,
    status      VARCHAR(20)  NOT NULL,
    message     TEXT,
    rows_count  INTEGER,
    duration_ms INTEGER,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_clean_sales_date     ON clean_sales(order_date);
CREATE INDEX IF NOT EXISTS idx_clean_sales_category ON clean_sales(category);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_date   ON daily_metrics(metric_date);
CREATE INDEX IF NOT EXISTS idx_pipeline_logs_status ON pipeline_logs(status);
