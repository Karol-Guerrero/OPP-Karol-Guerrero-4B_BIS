-- Lab 7.1 - MySQL / MariaDB (XAMPP)
-- phpMyAdmin: pestaña "SQL" -> pega todo el script -> Continuar
-- (o pestaña "Importar" -> elige este archivo). Se puede ejecutar varias veces.

CREATE DATABASE IF NOT EXISTS login_system_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE login_system_db;

-- Usuarios (login)
CREATE TABLE IF NOT EXISTS users (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)  NOT NULL UNIQUE,
    passw    VARCHAR(50)  NOT NULL,
    nombre   VARCHAR(100) NOT NULL
);

INSERT INTO users (username, passw, nombre)
VALUES ('admin', 'admin123', 'Super admin')
ON DUPLICATE KEY UPDATE username = username;

-- Paso 1: tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)  NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock  INT           NOT NULL
);

-- Paso 2: datos de ejemplo (solo si la tabla está vacía)
INSERT INTO productos (nombre, precio, stock)
SELECT * FROM (
    SELECT 'Laptop HP' AS nombre, 12500.50 AS precio, 10 AS stock
    UNION ALL SELECT 'Mouse Inalámbrico', 350.00, 25
    UNION ALL SELECT 'Teclado Mecánico', 850.00, 15
) AS v
WHERE NOT EXISTS (SELECT 1 FROM productos);

-- Verificación
SELECT * FROM users;
SELECT * FROM productos;
