-- Скрипт инициализации БД

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    second_name VARCHAR(100) NOT NULL,
    birthdate DATE,
    gender VARCHAR(10),
    biography TEXT,
    city VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
