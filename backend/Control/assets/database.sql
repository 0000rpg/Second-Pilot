CREATE OR REPLACE TABLE User (
    user_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(20),
    email VARCHAR(40),
    pass_hash VARCHAR(72),
)