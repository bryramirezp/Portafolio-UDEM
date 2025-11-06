from flask import Flask, Response, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import decimal
import datetime
import xml.etree.ElementTree as ET
import os
import sys

app = Flask(__name__)
CORS(app)

# Configuración usando variables de entorno para Docker
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'raul')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '123')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'joyeria_db')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def value_to_str(value):
    if isinstance(value, decimal.Decimal):
        return str(value)
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if value is None:
        return ''
    # Escapar caracteres especiales para XML
    return str(value).replace('&', '&').replace('<', '<').replace('>', '>').replace('"', '"').replace("'", "'")

def generate_xml_response(data, root_tag):
    """Genera respuesta XML usando xml.etree.ElementTree"""
    print(f"DEBUG: generate_xml_response called with data type: {type(data)}", file=sys.stderr)
    print(f"DEBUG: data = {data}", file=sys.stderr)
    if isinstance(data, list) and data:
        print(f"DEBUG: First item in list type: {type(data[0])}", file=sys.stderr)
    elif not isinstance(data, list):
        print(f"DEBUG: Single item type: {type(data)}", file=sys.stderr)

    root = ET.Element(root_tag)

    if isinstance(data, (list, tuple)):
        for item in data:
            item_elem = ET.SubElement(root, 'product')  # Use consistent 'product' tag
            if isinstance(item, dict):
                for key, val in item.items():
                    safe_value = value_to_str(val)
                    ET.SubElement(item_elem, key).text = safe_value
            elif isinstance(item, tuple):
                # Assume tuple order matches SELECT order: id, codigo, nombre, descripcion, precio, stock, material, marca, kilates
                keys = ['id', 'codigo', 'nombre', 'descripcion', 'precio', 'stock', 'material', 'marca', 'kilates']
                for i, val in enumerate(item):
                    if i < len(keys):
                        safe_value = value_to_str(val)
                        ET.SubElement(item_elem, keys[i]).text = safe_value
            else:
                print(f"DEBUG: Unsupported item type: {type(item)}", file=sys.stderr)
                # Fallback: treat as dict if possible
                if hasattr(item, 'items'):
                    for key, val in item.items():
                        safe_value = value_to_str(val)
                        ET.SubElement(item_elem, key).text = safe_value
    else:
        # Single item
        if isinstance(data, dict):
            for key, val in data.items():
                safe_value = value_to_str(val)
                ET.SubElement(root, key).text = safe_value
        elif isinstance(data, tuple):
            keys = ['id', 'codigo', 'nombre', 'descripcion', 'precio', 'stock', 'material', 'marca', 'kilates']
            for i, val in enumerate(data):
                if i < len(keys):
                    safe_value = value_to_str(val)
                    ET.SubElement(root, keys[i]).text = safe_value
        else:
            print(f"DEBUG: Unsupported single item type: {type(data)}", file=sys.stderr)

    xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
    print(f"DEBUG: Generated XML: {xml_str}", file=sys.stderr)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        print("DEBUG: Intentando conectar a la base de datos...")
        cur = mysql.connection.cursor()
        print("DEBUG: Cursor creado, ejecutando query...")
        cur.execute("SELECT id, codigo, nombre, descripcion, precio, stock, material, marca, kilates FROM products")
        products = cur.fetchall()
        print(f"DEBUG: Query ejecutada, {len(products)} productos encontrados")
        cur.close()

        print("DEBUG: Generando respuesta XML...")
        xml_output = generate_xml_response(products, 'products')
        print("DEBUG: Respuesta XML generada correctamente")
        print(f"DEBUG: XML output length: {len(xml_output)}")
        return Response(xml_output, mimetype='application/xml')

    except Exception as e:
        print(f"DEBUG: Error en get_products: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, codigo, nombre, descripcion, precio, stock, material, marca, kilates FROM products WHERE id = %s", (product_id,))
        product = cur.fetchone()
        cur.close()

        if not product:
            return Response('<error>Producto no encontrado</error>', mimetype='application/xml', status=404)

        xml_output = generate_xml_response(product, 'product')
        return Response(xml_output, mimetype='application/xml')

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

@app.route('/api/products/kilates/<int:kilates>', methods=['GET'])
def get_products_by_kilates(kilates):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, codigo, nombre, descripcion, precio, stock, material, marca, kilates FROM products WHERE kilates = %s", (kilates,))
        products = cur.fetchall()
        cur.close()

        xml_output = generate_xml_response(products, 'products')
        return Response(xml_output, mimetype='application/xml')

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

@app.route('/api/products/marca/<marca>', methods=['GET'])
def get_products_by_marca(marca):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, codigo, nombre, descripcion, precio, stock, material, marca, kilates FROM products WHERE marca = %s", (marca,))
        products = cur.fetchall()
        cur.close()

        xml_output = generate_xml_response(products, 'products')
        return Response(xml_output, mimetype='application/xml')

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

@app.route('/api/products/material/<material>', methods=['GET'])
def get_products_by_material(material):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, codigo, nombre, descripcion, precio, stock, material, marca, kilates FROM products WHERE material = %s", (material,))
        products = cur.fetchall()
        cur.close()

        xml_output = generate_xml_response(products, 'products')
        return Response(xml_output, mimetype='application/xml')

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

@app.route('/api/products/create', methods=['POST'])
def create_product():
    try:
        xml_data = request.data.decode('utf-8')
        if not xml_data:
            return Response('<error>Datos XML requeridos</error>', mimetype='application/xml', status=400)

        # Parsear XML
        root = ET.fromstring(xml_data)
        data = {}
        for child in root:
            data[child.tag] = child.text

        # Validar código único
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM products WHERE codigo = %s", (data.get('codigo'),))
        if cur.fetchone():
            cur.close()
            return Response('<error>Código de producto ya existe</error>', mimetype='application/xml', status=400)

        # Insertar producto
        cur.execute("""
            INSERT INTO products (codigo, nombre, descripcion, precio, stock, material, marca, kilates)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('codigo'), data.get('nombre'), data.get('descripcion', ''),
            data.get('precio'), data.get('stock'), data.get('material'), data.get('marca'), data.get('kilates')
        ))
        mysql.connection.commit()
        product_id = cur.lastrowid
        cur.close()

        return Response(f'<success>Producto creado con ID {product_id}</success>', mimetype='application/xml', status=201)

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        xml_data = request.data.decode('utf-8')
        if not xml_data:
            return Response('<error>Datos XML requeridos</error>', mimetype='application/xml', status=400)

        # Parsear XML
        root = ET.fromstring(xml_data)
        data = {}
        for child in root:
            data[child.tag] = child.text

        cur = mysql.connection.cursor()

        # Verificar que el producto existe
        cur.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        if not cur.fetchone():
            cur.close()
            return Response('<error>Producto no encontrado</error>', mimetype='application/xml', status=404)

        # Actualizar producto
        cur.execute("""
            UPDATE products SET
                codigo = %s, nombre = %s, descripcion = %s, precio = %s,
                stock = %s, material = %s, marca = %s, kilates = %s
            WHERE id = %s
        """, (
            data.get('codigo'), data.get('nombre'), data.get('descripcion', ''),
            data.get('precio'), data.get('stock'), data.get('material'), data.get('marca'), data.get('kilates'), product_id
        ))
        mysql.connection.commit()
        cur.close()

        return Response('<success>Producto actualizado</success>', mimetype='application/xml', status=200)

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        cur = mysql.connection.cursor()

        # Verificar que el producto existe
        cur.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        if not cur.fetchone():
            cur.close()
            return Response('<error>Producto no encontrado</error>', mimetype='application/xml', status=404)

        # Eliminar producto
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        mysql.connection.commit()
        cur.close()

        return Response('<success>Producto eliminado</success>', mimetype='application/xml', status=200)

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
