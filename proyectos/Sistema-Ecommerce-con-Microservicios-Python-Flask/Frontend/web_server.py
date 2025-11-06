from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def serve_index():
    return send_from_directory(base_dir, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(base_dir, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)