# Geopixelis - Tienda de Arte Espacial

Geopixelis es una aplicación web desarrollada con Flask que permite mostrar y vender productos artísticos basados en imágenes satelitales. Incluye un panel administrativo para gestionar los productos y un sistema de carrito de compras funcional.

---

## Estructura general del proyecto

### `app.py`
Archivo principal que contiene toda la lógica de la aplicación.

- Define las rutas (`/`, `/admin`, `/agregar`, `/editar/<id>`, `/eliminar/<id>`, `/carrito`, etc.).
- Carga y guarda los productos desde el archivo `productos.json`.
- Usa `session` para almacenar el carrito temporalmente.
- Controla el flujo entre las plantillas HTML y la lógica del backend.

---

### `productos.json`
Archivo de almacenamiento local que actúa como una base de datos sencilla.

- Contiene una lista de productos con campos como:
  - `id`: Identificador único.
  - `nombre`: Nombre del producto.
  - `precio`: Precio del cuadro.
  - `imagen`: Ruta de la imagen en `/static`.
  - `descripcion`: Información opcional del producto.
- Se actualiza automáticamente al agregar, editar o eliminar productos desde el panel de administración.

---

### `/templates/`
Carpeta que contiene las plantillas HTML renderizadas por Flask usando Jinja2.

- `index.html`: Página principal con el catálogo de productos y botón para añadir al carrito.
- `admin.html`: Vista de administración con la lista de productos y botones para editar o eliminar.
- `agregar.html`: Formulario para crear un nuevo producto.
- `editar.html`: Formulario que permite modificar un producto existente.
- `carrito.html`: Vista del carrito de compras, con resumen y botón de confirmar compra.

---

### `/static/`
Carpeta donde se guardan las imágenes de los productos y recursos visuales.

- Las rutas de imagen usadas en los productos apuntan a archivos ubicados aquí.
- Permite que las imágenes se carguen correctamente en el frontend.

---

## ¿Cómo funciona?

1. El usuario navega por el catálogo en la página principal (`/`).
2. Puede añadir productos al carrito (almacenado en `session`).
3. En el panel de administración (`/admin`), el administrador puede:
   - Agregar nuevos productos.
   - Editar información existente.
   - Eliminar productos.
4. Todos los cambios se reflejan automáticamente en `productos.json`.

---

## Requisitos

Para ejecutar el proyecto localmente:

```bash
pip install -r requirements.txt
python app.py
