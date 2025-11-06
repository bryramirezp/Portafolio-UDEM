-- init.sql para Dockerfile personalizado
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS jwt_auth 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE jwt_auth;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Verificar que las tablas se crearon
SHOW TABLES;