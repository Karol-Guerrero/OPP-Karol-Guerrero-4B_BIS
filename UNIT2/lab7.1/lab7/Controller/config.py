import os

# Datos de conexión a MySQL/MariaDB de XAMPP.
# Por defecto XAMPP usa: usuario "root", SIN contraseña y puerto 3306
# (si el puerto 3306 estaba ocupado, XAMPP puede usar 3307: míralo en su panel).
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "login_system_db"),
    "charset": "utf8mb4",
}
