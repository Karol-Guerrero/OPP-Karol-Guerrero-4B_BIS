-- Lab 8 - Login MVC (XAMPP: MySQL / MariaDB)
-- phpMyAdmin: pestaña "SQL" -> pega todo el script -> Continuar
-- (o pestaña "Importar" -> elige este archivo). Se puede ejecutar varias veces.

CREATE DATABASE IF NOT EXISTS login_mvc
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE login_mvc;

CREATE TABLE IF NOT EXISTS users (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    nombre   VARCHAR(100) NOT NULL,
    email    VARCHAR(100) NOT NULL UNIQUE,   -- UNIQUE: el modelo detecta correos duplicados
    password VARCHAR(255) NOT NULL
);

-- Usuario de prueba (opcional)
INSERT INTO users (nombre, email, password)
VALUES ('Administrador', 'admin@correo.com', 'admin123')
ON DUPLICATE KEY UPDATE email = email;

-- Verificación
SELECT id, nombre, email FROM users;
