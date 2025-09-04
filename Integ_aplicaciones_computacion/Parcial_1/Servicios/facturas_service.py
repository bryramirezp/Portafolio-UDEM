from flask import Flask, request, jsonify, Response
from flask_mysqldb import MySQL
from flask_cors import CORS
import uuid
import datetime
import decimal

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'joyeria_user'
app.config['MYSQL_PASSWORD'] = 'password_seguro'
app.config['MYSQL_DB'] = 'joyeria_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def value_to_str(value):
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    if isinstance(value, decimal.Decimal):
        return str(value)
    if value is None:
        return ""
    return str(value)

@app.route('/api/facturas', methods=['POST'])
def create_factura():
    try:
        data = request.get_json()
        if not data:
            return Response('<error>No se recibieron datos JSON.</error>', mimetype='application/xml', status=400)
        
        pedido_id = data.get('pedido_id')
        if not pedido_id:
            return Response('<error>El campo pedido_id es requerido.</error>', mimetype='application/xml', status=400)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pedidos WHERE id = %s", (pedido_id,))
        pedido = cur.fetchone()

        if not pedido:
            return Response(f'<error>Pedido con ID {pedido_id} no encontrado.</error>', mimetype='application/xml', status=404)

        folio = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO facturas (pedido_id, folio, subtotal, impuestos, total) VALUES (%s, %s, %s, %s, %s)",
            (pedido_id, folio, pedido['subtotal'], pedido['impuestos'], pedido['total'])
        )
        factura_id = cur.lastrowid
        mysql.connection.commit()

        cur.execute("SELECT * FROM clientes WHERE id = %s", (pedido['cliente_id'],))
        cliente = cur.fetchone()
        cur.execute("SELECT p.nombre, p.codigo, pd.cantidad, pd.precio_unitario FROM pedidos_detalle pd JOIN products p ON pd.producto_id = p.id WHERE pd.pedido_id = %s", (pedido_id,))
        items_detalle = cur.fetchall()
        cur.close()

        xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_output += '<factura>\n'
        xml_output += f'  <encabezado>\n'
        xml_output += f'    <id>{factura_id}</id>\n'
        xml_output += f'    <folio>{folio}</folio>\n'
        xml_output += f'    <fecha>{value_to_str(pedido["fecha"])}</fecha>\n'
        xml_output += '  </encabezado>\n'
        xml_output += f'  <cliente>\n'
        xml_output += f'    <nombre>{cliente["nombre"]}</nombre>\n'
        xml_output += f'    <email>{cliente["email"]}</email>\n'
        xml_output += '  </cliente>\n'
        xml_output += '  <items>\n'
        for item in items_detalle:
            importe = item['precio_unitario'] * item['cantidad']
            xml_output += '    <item>\n'
            xml_output += f'      <codigo>{item["codigo"]}</codigo>\n'
            xml_output += f'      <nombre>{item["nombre"]}</nombre>\n'
            xml_output += f'      <cantidad>{item["cantidad"]}</cantidad>\n'
            xml_output += f'      <precio_unitario>{value_to_str(item["precio_unitario"])}</precio_unitario>\n'
            xml_output += f'      <importe>{value_to_str(importe)}</importe>\n'
            xml_output += '    </item>\n'
        xml_output += '  </items>\n'
        xml_output += '  <totales>\n'
        xml_output += f'    <subtotal>{value_to_str(pedido["subtotal"])}</subtotal>\n'
        xml_output += f'    <impuestos>{value_to_str(pedido["impuestos"])}</impuestos>\n'
        xml_output += f'    <total>{value_to_str(pedido["total"])}</total>\n'
        xml_output += '  </totales>\n'
        xml_output += '</factura>'

        return Response(xml_output, mimetype='application/xml')

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

