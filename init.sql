CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    customer_id VARCHAR(255),
    customer_group_id VARCHAR(255),
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP NOT NULL
);

CREATE INDEX idx_product_id ON prices(product_id);
CREATE INDEX idx_currency ON prices(currency);
CREATE INDEX idx_customer_id ON prices(customer_id);
CREATE INDEX idx_customer_group_id ON prices(customer_group_id);
CREATE INDEX idx_valid_from ON prices(valid_from);
CREATE INDEX idx_valid_to ON prices(valid_to);
CREATE INDEX idx_price_lookup ON prices(product_id, currency, customer_id, valid_from, valid_to);
