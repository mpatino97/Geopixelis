'''
Geopixelis - Aplicación web de venta de arte satelital

Este archivo contiene la lógica del backend desarrollada con Flask.
Incluye funcionalidades para la visualización de productos, administración,
carrito de compras y persistencia de datos en formato JSON.

Desarrollador: Maicol Patiño
Fecha: 2025-07-20
Versión: 1.0
'''

from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'secret0123'
app.config['JSON_AS_ASCII'] = False  # Permitir caracteres especiales en JSON

# Ruta al archivo de productos (persistencia local)
DB_FILE = 'productos.json'

# ---------------------------
# Funciones de utilidad
# ---------------------------

def cargar_productos():
    """
    Carga la lista de productos desde un archivo JSON.
    Si el archivo no existe, lo crea con una lista vacía.

    Returns:
        list: Lista de productos (diccionarios).
    """
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_productos(productos):
    """
    Guarda la lista de productos en el archivo JSON.

    Args:
        productos (list): Lista de productos actualizada.
    """
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

def obtener_contador_carrito():
    """
    Calcula el total de ítems en el carrito actual de la sesión.

    Returns:
        int: Cantidad total de productos en el carrito.
    """
    return sum(item.get('cantidad', 1) for item in session.get('carrito', []))

# ---------------------------
# Rutas principales del sitio
# ---------------------------

@app.route('/')
def index():
    """
    Vista principal de la tienda.
    Carga y muestra todos los productos disponibles.
    """
    productos = cargar_productos()
    carrito = session.get('carrito', [])
    contador = obtener_contador_carrito()
    return render_template('index.html', productos=productos, carrito=carrito, contador=contador)

@app.route('/agregar_carrito/<int:id>')
def agregar_carrito(id):
    """
    Agrega un producto al carrito de compras mediante su ID.

    Args:
        id (int): ID del producto a agregar.
    """
    productos = cargar_productos()
    producto = next((p for p in productos if p['id'] == id), None)
    if not producto:
        return "Producto no encontrado", 404

    carrito = session.get('carrito', [])
    for item in carrito:
        if item['id'] == id:
            item['cantidad'] += 1
            break
    else:
        producto['cantidad'] = 1
        carrito.append(producto)

    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('index'))

@app.route('/carrito')
def ver_carrito():
    """
    Muestra el contenido actual del carrito.
    Calcula el total a pagar.
    """
    carrito = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    contador = obtener_contador_carrito()
    return render_template('carrito.html', carrito=carrito, total=total, contador=contador)

@app.route('/quitar_del_carrito/<int:producto_id>')
def quitar_del_carrito(producto_id):
    """
    Elimina un producto del carrito por su ID.
    """
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['id'] != producto_id]
    session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

@app.route('/vaciar_carrito')
def vaciar_carrito():
    """
    Vacía completamente el carrito de la sesión actual.
    """
    session['carrito'] = []
    return redirect(url_for('ver_carrito'))

@app.route('/confirmar_compra', methods=['GET', 'POST'])
def confirmar_compra():
    """
    Procesa la confirmación de la compra.
    Si el método es POST, se limpia el carrito y se muestra un mensaje.
    """
    if request.method == 'POST':
        cantidad = int(request.form.get('carrito', 0))
        print(f"Compra confirmada con {cantidad} producto(s)")
        session.pop('carrito', None)
        session['carrito_confirmado'] = cantidad
        flash("Compra realizada exitosamente.")
        return redirect(url_for('index'))
    else:
        session.pop('carrito', None)
        return render_template('compra_exitosa.html', contador=0)

# ---------------------------
# Rutas para Administración
# ---------------------------

@app.route('/admin')
def admin():
    """
    Vista del panel de administración.
    Lista todos los productos con opción de editar o eliminar.
    """
    productos = cargar_productos()
    return render_template('admin.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    """
    Vista para agregar un nuevo producto.
    En POST guarda el producto enviado por el formulario.
    """
    if request.method == 'POST':
        productos = cargar_productos()
        nuevo_id = max([p['id'] for p in productos], default=0) + 1
        nuevo_producto = {
            'id': nuevo_id,
            'nombre': request.form['nombre'],
            'description': request.form['description'],
            'precio': float(request.form['precio']),
            'imagen': request.form['imagen']
        }
        productos.append(nuevo_producto)
        guardar_productos(productos)
        flash("Producto agregado correctamente.")
        return redirect(url_for('admin'))
    return render_template('agregar.html')

@app.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar(producto_id):
    """
    Vista para editar un producto existente.

    Args:
        producto_id (int): ID del producto a editar.
    """
    productos = cargar_productos()
    producto = next((p for p in productos if p["id"] == producto_id), None)

    if not producto:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        producto["nombre"] = request.form["nombre"]
        producto["description"] = request.form["description"]
        producto["precio"] = float(request.form["precio"])
        producto["imagen"] = request.form["imagen"]

        guardar_productos(productos)
        flash("Producto actualizado correctamente.")
        return redirect(url_for('admin'))

    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:producto_id>', methods=['POST'])
def eliminar(producto_id):
    """
    Elimina un producto del archivo JSON.

    Args:
        producto_id (int): ID del producto a eliminar.
    """
    productos = cargar_productos()
    productos = [p for p in productos if p['id'] != producto_id]
    guardar_productos(productos)
    flash("Producto eliminado.")
    return redirect(url_for('admin'))

# ---------------------------
# Punto de entrada
# ---------------------------

if __name__ == '__main__':
    app.run(debug=True)
