from flask import Flask, Response, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import decimal
import datetime

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'joyeria_user'
app.config['MYSQL_PASSWORD'] = 'password_seguro'
app.config['MYSQL_DB'] = 'joyeria_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def value_to_str(value):
    if isinstance(value, decimal.Decimal):
        return str(value)
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if value is None:
        return ''
    return str(value)

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, codigo, nombre, descripcion, precio, stock, material, marca, kilates FROM products")
        products = cur.fetchall()
        cur.close()
        
        xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n<products>\n'
        
        for product in products:
            xml_output += '  <product>\n'
            for key, val in product.items():
                safe_value = value_to_str(val)
                xml_output += f'    <{key}>{safe_value}</{key}>\n'
            xml_output += '  </product>\n'
            
        xml_output += '</products>'
        
        return Response(xml_output, mimetype='application/xml')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
