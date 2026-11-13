-- Lab 9 - Login MVC + Productos (XAMPP: MySQL / MariaDB)
-- phpMyAdmin: pestaña "SQL" -> pega todo el script -> Continuar
-- (o pestaña "Importar" -> elige este archivo). Se puede ejecutar varias veces.

CREATE DATABASE IF NOT EXISTS login_mvc
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE login_mvc;

-- Usuarios (login)
CREATE TABLE IF NOT EXISTS users (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    nombre   VARCHAR(100) NOT NULL,
    email    VARCHAR(100) NOT NULL UNIQUE,   -- UNIQUE: el modelo detecta correos duplicados
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (nombre, email, password)
VALUES ('Administrador', 'admin@correo.com', 'admin123')
ON DUPLICATE KEY UPDATE email = email;

-- Productos (los que se exportan a CSV, TXT, JSON y PDF)
CREATE TABLE IF NOT EXISTS productos (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)  NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock  INT           NOT NULL
);

-- Datos de ejemplo (solo si la tabla está vacía)
INSERT INTO productos (nombre, precio, stock)
SELECT * FROM (
    SELECT 'Laptop HP' AS nombre, 12500.50 AS precio, 10 AS stock
    UNION ALL SELECT 'Mouse Inalámbrico', 350.00, 25
    UNION ALL SELECT 'Teclado Mecánico', 850.00, 15
) AS v
WHERE NOT EXISTS (SELECT 1 FROM productos);

-- Verificación
SELECT id, nombre, email FROM users;
SELECT * FROM productos;
