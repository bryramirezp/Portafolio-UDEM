from flask import Flask, request, Response
from flask_mysqldb import MySQL
from flask_cors import CORS
import datetime
import decimal
import xml.etree.ElementTree as ET
import os

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
        xml_data = request.data.decode('utf-8')
        if not xml_data:
            return Response('<error>No se recibieron datos XML.</error>', mimetype='application/xml', status=400)

        # Parsear XML
        root = ET.fromstring(xml_data)
        pedido_id_elem = root.find('pedido_id')
        if pedido_id_elem is None or pedido_id_elem.text is None:
            return Response('<error>El campo pedido_id es requerido.</error>', mimetype='application/xml', status=400)
        pedido_id = int(pedido_id_elem.text)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pedidos WHERE id = %s", (pedido_id,))
        pedido = cur.fetchone()

        if not pedido:
            return Response(f'<error>Pedido con ID {pedido_id} no encontrado.</error>', mimetype='application/xml', status=404)

        # Generar folio único con formato FAC-YYYYMMDD-<id>
        # Nota: factura_id se genera después del INSERT, por lo que usamos un contador temporal
        from datetime import datetime
        fecha_actual = datetime.now().strftime('%Y%m%d')

        # Obtener el último ID de factura para generar el siguiente
        cur.execute("SELECT COALESCE(MAX(id), 0) + 1 as next_id FROM facturas")
        next_id_result = cur.fetchone()
        next_folio_id = next_id_result['next_id']

        folio = f"FAC-{fecha_actual}-{next_folio_id}"
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

@app.route('/api/facturas/<int:factura_id>', methods=['GET'])
def get_factura_by_id(factura_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM facturas WHERE id = %s", (factura_id,))
        factura = cur.fetchone()

        if not factura:
            cur.close()
            return Response('<error>Factura no encontrada</error>', mimetype='application/xml', status=404)

        # Obtener datos del pedido
        cur.execute("SELECT * FROM pedidos WHERE id = %s", (factura['pedido_id'],))
        pedido = cur.fetchone()

        # Obtener datos del cliente
        cur.execute("SELECT * FROM clientes WHERE id = %s", (pedido['cliente_id'],))
        cliente = cur.fetchone()

        # Obtener detalles de productos
        cur.execute("""
            SELECT p.nombre, p.codigo, pd.cantidad, pd.precio_unitario
            FROM pedidos_detalle pd
            JOIN products p ON pd.producto_id = p.id
            WHERE pd.pedido_id = %s
        """, (factura['pedido_id'],))
        items_detalle = cur.fetchall()
        cur.close()

        # Respuesta XML usando ET
        root = ET.Element('factura')

        # Encabezado
        encabezado = ET.SubElement(root, 'encabezado')
        ET.SubElement(encabezado, 'id').text = str(factura['id'])
        ET.SubElement(encabezado, 'folio').text = factura['folio']
        ET.SubElement(encabezado, 'fecha').text = value_to_str(factura['fecha'])

        # Cliente
        cliente_elem = ET.SubElement(root, 'cliente')
        ET.SubElement(cliente_elem, 'nombre').text = cliente['nombre']
        ET.SubElement(cliente_elem, 'email').text = cliente['email']

        # Items
        items_elem = ET.SubElement(root, 'items')
        for item in items_detalle:
            item_elem = ET.SubElement(items_elem, 'item')
            importe = item['precio_unitario'] * item['cantidad']
            ET.SubElement(item_elem, 'codigo').text = item['codigo']
            ET.SubElement(item_elem, 'nombre').text = item['nombre']
            ET.SubElement(item_elem, 'cantidad').text = str(item['cantidad'])
            ET.SubElement(item_elem, 'precio_unitario').text = value_to_str(item['precio_unitario'])
            ET.SubElement(item_elem, 'importe').text = value_to_str(importe)

        # Totales
        totales = ET.SubElement(root, 'totales')
        ET.SubElement(totales, 'subtotal').text = value_to_str(factura['subtotal'])
        ET.SubElement(totales, 'impuestos').text = value_to_str(factura['impuestos'])
        ET.SubElement(totales, 'total').text = value_to_str(factura['total'])

        xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
        xml_output = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
        return Response(xml_output, mimetype='application/xml')

    except Exception as e:
        return Response(f'<error>Error interno del servidor: {str(e)}</error>', mimetype='application/xml', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

