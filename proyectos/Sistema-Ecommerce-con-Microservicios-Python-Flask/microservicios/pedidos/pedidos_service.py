from flask import Flask, request, Response
from flask_mysqldb import MySQL
from flask_cors import CORS
from decimal import Decimal, InvalidOperation
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

# Configuración usando variables de entorno para Docker
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'raul')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '123')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'joyeria_db')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/api/pedidos', methods=['POST'])
def create_pedido():
    try:
        xml_data = request.data.decode('utf-8')
        if not xml_data:
            return Response('<response><error>Datos XML requeridos</error></response>', mimetype='application/xml', status=400)

        # Parsear XML
        root = ET.fromstring(xml_data)
        cliente_id = int(root.find('cliente_id').text)
        items = []
        for item_elem in root.findall('item'):
            item = {
                'id': int(item_elem.find('id').text),
                'cantidad': int(item_elem.find('cantidad').text)
            }
            items.append(item)

        if not items:
            return Response('<response><error>El carrito está vacío</error></response>', mimetype='application/xml', status=400)

        subtotal = Decimal('0.0')
        product_cache = {}  # Cache para evitar queries redundantes

        cur = mysql.connection.cursor()

        # Validar stock disponible y calcular subtotal
        for item in items:
            if item['id'] not in product_cache:
                cur.execute("SELECT precio, stock FROM products WHERE id = %s", (item['id'],))
                product = cur.fetchone()
                if not product:
                    cur.close()
                    return Response(f'<response><error>Producto con ID {item["id"]} no encontrado</error></response>', mimetype='application/xml', status=404)
                product_cache[item['id']] = product

            product = product_cache[item['id']]
            cantidad_solicitada = Decimal(item['cantidad'])
            stock_disponible = Decimal(product['stock'])

            if cantidad_solicitada > stock_disponible:
                cur.close()
                return Response(f'<response><error>Stock insuficiente para producto ID {item["id"]}. Disponible: {stock_disponible}, solicitado: {cantidad_solicitada}</error></response>', mimetype='application/xml', status=400)

            precio_unitario = product['precio']
            subtotal += precio_unitario * cantidad_solicitada

        impuestos = subtotal * Decimal('0.16')
        total = subtotal + impuestos

        # Usar transacción para atomicidad
        cur.execute("START TRANSACTION")

        try:
            cur.execute(
                "INSERT INTO pedidos (cliente_id, subtotal, impuestos, total) VALUES (%s, %s, %s, %s)",
                (cliente_id, subtotal, impuestos, total)
            )
            pedido_id = cur.lastrowid

            # Insertar detalles del pedido y descontar stock
            for item in items:
                product = product_cache[item['id']]
                precio_unitario = product['precio']

                # Insertar detalle del pedido
                cur.execute(
                    "INSERT INTO pedidos_detalle (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                    (pedido_id, item['id'], item['cantidad'], precio_unitario)
                )

                # Descontar stock del producto
                cur.execute(
                    "UPDATE products SET stock = stock - %s WHERE id = %s",
                    (item['cantidad'], item['id'])
                )

            cur.execute("COMMIT")
            cur.close()

            xml_response = f'<response><status>success</status><pedido_id>{pedido_id}</pedido_id><total>{float(total)}</total></response>'
            return Response(xml_response, mimetype='application/xml')

        except Exception as e:
            cur.execute("ROLLBACK")
            cur.close()
            raise e

    except (InvalidOperation, TypeError) as e:
        return Response(f'<response><error>Error de tipo de dato: {e}</error></response>', mimetype='application/xml', status=400)
    except Exception as e:
        return Response(f'<response><error>Error interno del servidor: {e}</error></response>', mimetype='application/xml', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
