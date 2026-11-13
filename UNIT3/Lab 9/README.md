# Lab 9 – Módulo de exportación (CSV, TXT, JSON y PDF)

Proyecto MVC (login + productos) con exportación de los productos de la base de datos.
En la pantalla de productos se elige el formato en un **Combobox de solo lectura**
(CSV, TXT, JSON, PDF) y se pulsa **Exportar Reporte**.

## Estructura
```
Lab 9/
├── main.py                              # arranca la app y conecta las piezas
├── exporters.py                         # TODA la lógica de archivos (csv, json, fpdf)
├── controllers/
│   ├── conexion_controller.py           # conexión a MySQL (XAMPP)
│   ├── authentication_controller.py     # login / registro
│   └── products_controller.py           # tabla, guardar y generar_reporte(formato)
├── models/
│   ├── user_model.py
│   ├── products_model.py
│   └── squema.sql                       # base login_mvc: users + productos
└── views/
    ├── login_view.py
    ├── register_view.py
    └── home_view.py                     # tabla, formulario, Combobox y botón "Exportar Reporte"
```

## Cómo correrlo
1. Entorno virtual e instalación: `pip install -r requirements.txt` (incluye `pip install fpdf`).
2. En XAMPP inicia **MySQL** y ejecuta `models/squema.sql` en phpMyAdmin (pestaña SQL).
3. `python main.py` y entra con **admin@correo.com / admin123**.
4. Elige el formato, pulsa **Exportar Reporte** y escoge dónde guardar el archivo.

## Diseño (herencia y polimorfismo)
- `Exporter` es la clase base abstracta: su método `export(data, file_path)` lanza
  `NotImplementedError` si una clase hija no lo sobrescribe (hace de interfaz).
- `CSVExporter` (csv), `TXTExporter` (open), `JSONExporter` (json) y `PDFExporter` (fpdf)
  heredan de `Exporter` y sobrescriben `export()` con la lógica de su formato.
- `ProductsController.generar_reporte(formato)` instancia **solo** la clase hija elegida
  (`EXPORTERS[formato]()`) y llama `.export(productos, ruta)`; no sabe qué formato se genera.

## Regla del lab
Ningún archivo, salvo `exporters.py`, importa `csv`, `json` ni `fpdf`.
