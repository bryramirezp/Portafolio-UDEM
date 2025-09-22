from flask import Flask, request, jsonify, Response
from flask_mysqldb import MySQL
from flask_cors import CORS
from decimal import Decimal, InvalidOperation

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'joyeria_user'
app.config['MYSQL_PASSWORD'] = 'password_seguro'
app.config['MYSQL_DB'] = 'joyeria_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/api/pedidos', methods=['POST'])
def create_pedido():
    try:
        data = request.get_json()
        cliente_id = data['cliente_id']
        items = data['items']
        
        if not items:
            return jsonify({'error': 'El carrito está vacío'}), 400

        subtotal = Decimal('0.0')
        
        cur = mysql.connection.cursor()

        for item in items:
            cur.execute("SELECT precio FROM products WHERE id = %s", (item['id'],))
            product = cur.fetchone()
            if product:
                precio_unitario = product['precio']
                cantidad = Decimal(item['cantidad'])
                subtotal += precio_unitario * cantidad
            else:
                return jsonify({'error': f"Producto con ID {item['id']} no encontrado"}), 404

        impuestos = subtotal * Decimal('0.16')
        total = subtotal + impuestos

        cur.execute(
            "INSERT INTO pedidos (cliente_id, subtotal, impuestos, total) VALUES (%s, %s, %s, %s)",
            (cliente_id, subtotal, impuestos, total)
        )
        pedido_id = cur.lastrowid
        
        for item in items:
            cur.execute("SELECT precio FROM products WHERE id = %s", (item['id'],))
            product = cur.fetchone()
            precio_unitario = product['precio']
            cur.execute(
                "INSERT INTO pedidos_detalle (pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                (pedido_id, item['id'], item['cantidad'], precio_unitario)
            )

        mysql.connection.commit()
        cur.close()

        return jsonify({'status': 'success', 'pedido_id': pedido_id, 'total': float(total)})

    except (InvalidOperation, TypeError) as e:
        return Response(f'<response><error>Error de tipo de dato: {e}</error></response>', mimetype='application/xml', status=400)
    except Exception as e:
        return Response(f'<response><error>Error interno del servidor: {e}</error></response>', mimetype='application/xml', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
