import os
import jwt
import datetime
import logging
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from dotenv import load_dotenv
from functools import wraps

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'UDEM')
app.config['ACCESS_TOKEN_EXPIRES_MINUTES'] = int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES', 15))
app.config['REFRESH_TOKEN_EXPIRES_DAYS'] = int(os.getenv('REFRESH_TOKEN_EXPIRES_DAYS', 7))

# Database connection con retry
def get_db_connection(max_retries=5, delay=2):
    for attempt in range(max_retries):
        try:
            connection = pymysql.connect(
                host=os.getenv('DB_HOST', 'mariadb'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER', 'jwt_user'),
                password=os.getenv('DB_PASSWORD', 'jwt_password'),
                database=os.getenv('DB_NAME', 'jwt_auth'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("Conexión a BD establecida exitosamente")
            return connection
        except pymysql.Error as e:
            logger.warning(f"Intento {attempt + 1} de conexión a BD falló: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                logger.error("No se pudo conectar a la BD después de varios intentos")
                raise

# Función de debug para la base de datos
def debug_database():
    """Función de debug para verificar el estado de la BD"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM tokens")
            count = cursor.fetchone()['count']
            logger.info(f"DEBUG - Tokens en BD: {count}")
        connection.close()
    except Exception as e:
        logger.error(f"DEBUG - Error en BD: {e}")

# JWT token generator
def generate_token(user_id, token_type='access'):
    if token_type == 'access':
        expires_delta = datetime.timedelta(minutes=app.config['ACCESS_TOKEN_EXPIRES_MINUTES'])
    else:
        expires_delta = datetime.timedelta(days=app.config['REFRESH_TOKEN_EXPIRES_DAYS'])
    
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + expires_delta,
        'type': token_type,
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

# Token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                logger.warning("Authorization header malformed")
                return jsonify({'message': 'Token is missing!'}), 401

        if not token:
            logger.warning("No token provided")
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Verificar firma JWT
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            
            # Verificar en base de datos que el token no esté revocado
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM tokens WHERE user_id = %s AND access_token = %s AND is_revoked = FALSE AND expires_at > %s',
                    (current_user_id, token, datetime.datetime.utcnow())
                )
                token_record = cursor.fetchone()
            connection.close()
            
            if not token_record:
                logger.warning(f"Token invalid or revoked for user {current_user_id}")
                return jsonify({'message': 'Token is invalid or revoked!'}), 401
                
            logger.info(f"Token validated for user {current_user_id}")
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user_id, *args, **kwargs)

    return decorated

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        logger.warning("Registration failed: missing fields")
        return jsonify({'message': 'Missing username, email or password'}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE username = %s OR email = %s', (username, email))
            if cursor.fetchone():
                logger.warning(f"Registration failed: user already exists - {username}")
                return jsonify({'message': 'User already exists'}), 400

            # Insert new user (en producción, hashear la contraseña)
            cursor.execute(
                'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                (username, email, password)
            )
            connection.commit()
            user_id = cursor.lastrowid
            logger.info(f"User registered successfully: {username} (ID: {user_id})")
    except Exception as e:
        connection.rollback()
        logger.error(f"Database error during registration: {str(e)}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        connection.close()

    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201

@app.route('/login', methods=['POST'])
def login():
    # Debug antes del login
    debug_database()
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning("Login failed: missing credentials")
        return jsonify({'message': 'Missing username or password'}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Buscar usuario
            cursor.execute(
                'SELECT id, username, password FROM users WHERE username = %s',
                (username,)
            )
            user = cursor.fetchone()
            
            if not user:
                logger.warning(f"Login failed: user not found - {username}")
                return jsonify({'message': 'Invalid credentials'}), 401

            # Verificar contraseña (en producción usar hashing)
            if user['password'] != password:
                logger.warning(f"Login failed: invalid password for user - {username}")
                return jsonify({'message': 'Invalid credentials'}), 401

            user_id = user['id']

            # Generar tokens
            access_token = generate_token(user_id, 'access')
            refresh_token = generate_token(user_id, 'refresh')
            audit_token = generate_token(user_id, 'audit')

            # Calcular expiración
            access_token_expires = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=app.config['ACCESS_TOKEN_EXPIRES_MINUTES']
            )
            refresh_token_expires = datetime.datetime.utcnow() + datetime.timedelta(
                days=app.config['REFRESH_TOKEN_EXPIRES_DAYS']
            )

            # DEBUG: Log para verificar los tokens generados
            logger.info(f"Tokens generados para user_id {user_id}:")
            logger.info(f"Access Token: {access_token[:50]}...")
            logger.info(f"Refresh Token: {refresh_token[:50]}...")

            # Guardar tokens en la base de datos - VERSIÓN CORREGIDA
            cursor.execute(
                '''INSERT INTO tokens (user_id, access_token, refresh_token, audit_token, expires_at) 
                   VALUES (%s, %s, %s, %s, %s)''',
                (user_id, access_token, refresh_token, audit_token, access_token_expires)
            )
            
            # DEBUG: Verificar inserción
            if cursor.rowcount > 0:
                logger.info(f"✅ Token guardado en BD para user_id {user_id}")
                # Verificar que realmente se guardó
                cursor.execute("SELECT COUNT(*) as count FROM tokens WHERE user_id = %s", (user_id,))
                count_after = cursor.fetchone()['count']
                logger.info(f"DEBUG - Tokens para user_id {user_id} después de inserción: {count_after}")
            else:
                logger.error(f"❌ Error: Token NO guardado en BD para user_id {user_id}")

            connection.commit()
            logger.info(f"Login successful for user: {username} (ID: {user_id})")

    except Exception as e:
        connection.rollback()
        logger.error(f"Database error during login: {str(e)}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        connection.close()

    # Debug después del login
    debug_database()

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': app.config['ACCESS_TOKEN_EXPIRES_MINUTES'] * 60,
        'message': 'Login successful'
    }), 200

@app.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        logger.warning("Refresh failed: no refresh token provided")
        return jsonify({'message': 'Refresh token is missing'}), 400

    try:
        # Verificar refresh token JWT
        payload = jwt.decode(refresh_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        if payload['type'] != 'refresh':
            logger.warning("Refresh failed: invalid token type")
            return jsonify({'message': 'Invalid token type'}), 401

        user_id = payload['user_id']

        # Verificar en base de datos que el refresh_token no esté revocado
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM tokens WHERE user_id = %s AND refresh_token = %s AND is_revoked = FALSE',
                (user_id, refresh_token)
            )
            token_record = cursor.fetchone()

            if not token_record:
                logger.warning(f"Refresh failed: invalid or revoked refresh token for user {user_id}")
                return jsonify({'message': 'Invalid refresh token'}), 401

            # Verificar que el refresh token no haya expirado (en la BD)
            if token_record['expires_at'] and token_record['expires_at'] < datetime.datetime.utcnow():
                logger.warning(f"Refresh failed: refresh token expired for user {user_id}")
                return jsonify({'message': 'Refresh token has expired'}), 401

            # Generate new access token
            new_access_token = generate_token(user_id, 'access')
            new_access_token_expires = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=app.config['ACCESS_TOKEN_EXPIRES_MINUTES']
            )

            # Update ONLY the access token and its expiration in database
            cursor.execute(
                '''UPDATE tokens 
                   SET access_token = %s, expires_at = %s, created_at = %s 
                   WHERE user_id = %s AND refresh_token = %s AND is_revoked = FALSE''',
                (new_access_token, new_access_token_expires, datetime.datetime.utcnow(), user_id, refresh_token)
            )
            
            # Verificar actualización
            if cursor.rowcount > 0:
                logger.info(f"✅ Access token actualizado para user {user_id}")
            else:
                logger.error(f"❌ Error actualizando access token para user {user_id}")
                connection.rollback()
                return jsonify({'message': 'Error updating token'}), 500
                
            connection.commit()
            logger.info(f"Token refreshed for user: {user_id}")
            
        connection.close()

        return jsonify({
            'access_token': new_access_token,
            'token_type': 'Bearer',
            'expires_in': app.config['ACCESS_TOKEN_EXPIRES_MINUTES'] * 60,
            'message': 'Token refreshed successfully'
        }), 200

    except jwt.ExpiredSignatureError:
        logger.warning("Refresh failed: refresh token expired (JWT)")
        return jsonify({'message': 'Refresh token has expired'}), 401
    except jwt.InvalidTokenError as e:
        logger.warning(f"Refresh failed: invalid refresh token - {str(e)}")
        return jsonify({'message': 'Invalid refresh token'}), 401

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user_id):
    auth_header = request.headers['Authorization']
    token = auth_header.split(" ")[1]

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Marcar token como revocado
            cursor.execute(
                'UPDATE tokens SET is_revoked = TRUE WHERE user_id = %s AND access_token = %s',
                (current_user_id, token)
            )
            
            # Verificar revocación
            if cursor.rowcount > 0:
                logger.info(f"✅ Token revocado para user {current_user_id}")
            else:
                logger.warning(f"⚠ No se encontró token para revocar para user {current_user_id}")
                
            connection.commit()
            logger.info(f"User logged out: {current_user_id}")
    except Exception as e:
        connection.rollback()
        logger.error(f"Database error during logout: {str(e)}")
        return jsonify({'message': 'Database error'}), 500
    finally:
        connection.close()

    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user_id):
    logger.info(f"Protected endpoint accessed by user: {current_user_id}")
    return jsonify({
        'message': 'This is a protected endpoint',
        'user_id': current_user_id,
        'data': 'Secret data only for authenticated users'
    }), 200

# Health check endpoint mejorado
@app.route('/health', methods=['GET'])
def health():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            # Verificar también las tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
        connection.close()
        return jsonify({
            'status': 'healthy', 
            'database': 'connected',
            'tables': [table['Tables_in_jwt_auth'] for table in tables],
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy', 
            'database': 'disconnected',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Iniciando microservicio JWT...")
    app.run(host='0.0.0.0', port=5000, debug=False)