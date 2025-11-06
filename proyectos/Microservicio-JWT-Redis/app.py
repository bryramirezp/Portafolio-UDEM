import os
import jwt
import datetime
import logging
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import redis
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

# Redis client con retry
def get_redis_client(max_retries=5, delay=2):
    for attempt in range(max_retries):
        try:
            client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'redis'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                password=os.getenv('REDIS_PASSWORD', 'redis_password'),
                decode_responses=True
            )
            # Test connection
            client.ping()
            logger.info("Conexión a Redis establecida exitosamente")
            return client
        except redis.ConnectionError as e:
            logger.warning(f"Intento {attempt + 1} de conexión a Redis falló: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                logger.error("No se pudo conectar a Redis después de varios intentos")
                raise

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

# Función de debug para Redis
def debug_database():
    """Función de debug para verificar el estado de Redis"""
    try:
        redis_client = get_redis_client()
        access_count = len(redis_client.keys('access_token:*'))
        refresh_count = len(redis_client.keys('refresh_token:*'))
        logger.info(f"DEBUG - Access tokens en Redis: {access_count}")
        logger.info(f"DEBUG - Refresh tokens en Redis: {refresh_count}")
    except Exception as e:
        logger.error(f"DEBUG - Error en Redis: {e}")

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

            # Verificar en Redis que el token existe y no ha expirado
            redis_client = get_redis_client()
            token_key = f"access_token:{token}"

            if not redis_client.exists(token_key):
                logger.warning(f"Token not found in Redis for user {current_user_id}")
                return jsonify({'message': 'Token is invalid or revoked!'}), 401

            # Obtener el user_id almacenado en Redis para verificar
            stored_user_id = redis_client.get(token_key)
            if str(stored_user_id) != str(current_user_id):
                logger.warning(f"Token user_id mismatch for user {current_user_id}")
                return jsonify({'message': 'Token is invalid!'}), 401

            logger.info(f"Token validated for user {current_user_id}")

        except redis.ConnectionError:
            logger.error("Redis connection failed - token validation unavailable")
            return jsonify({'message': 'Service temporarily unavailable'}), 503

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

            # DEBUG: Log para verificar los tokens generados
            logger.info(f"Tokens generados para user_id {user_id}:")
            logger.info(f"Access Token: {access_token[:50]}...")
            logger.info(f"Refresh Token: {refresh_token[:50]}...")

            # Guardar tokens en Redis con TTL
            redis_client = get_redis_client()

            # Access token: 15 minutos
            access_ttl = app.config['ACCESS_TOKEN_EXPIRES_MINUTES'] * 60
            redis_client.setex(f"access_token:{access_token}", access_ttl, user_id)

            # Refresh token: 7 días
            refresh_ttl = app.config['REFRESH_TOKEN_EXPIRES_DAYS'] * 24 * 60 * 60
            redis_client.setex(f"refresh_token:{refresh_token}", refresh_ttl, user_id)

            # También guardar el refresh token asociado al access token para facilitar logout
            redis_client.setex(f"access_to_refresh:{access_token}", access_ttl, refresh_token)

            logger.info(f"✅ Tokens guardados en Redis para user_id {user_id}")
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

        # Verificar en Redis que el refresh_token existe
        redis_client = get_redis_client()
        refresh_key = f"refresh_token:{refresh_token}"

        if not redis_client.exists(refresh_key):
            logger.warning(f"Refresh failed: refresh token not found in Redis for user {user_id}")
            return jsonify({'message': 'Invalid refresh token'}), 401

        # Verificar que el user_id coincida
        stored_user_id = redis_client.get(refresh_key)
        if str(stored_user_id) != str(user_id):
            logger.warning(f"Refresh failed: user_id mismatch for user {user_id}")
            return jsonify({'message': 'Invalid refresh token'}), 401

        # Generate new access token
        new_access_token = generate_token(user_id, 'access')

        # Actualizar tokens en Redis
        # Access token: 15 minutos
        access_ttl = app.config['ACCESS_TOKEN_EXPIRES_MINUTES'] * 60
        redis_client.setex(f"access_token:{new_access_token}", access_ttl, user_id)

        # Mantener el refresh token (no cambiar TTL)
        # Actualizar la relación access_to_refresh
        redis_client.setex(f"access_to_refresh:{new_access_token}", access_ttl, refresh_token)

        logger.info(f"✅ Tokens actualizados en Redis para user {user_id}")
        logger.info(f"Token refreshed for user: {user_id}")

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
    access_token = auth_header.split(" ")[1]

    # Revocar token en Redis
    redis_client = get_redis_client()
    try:
        # Eliminar access token
        access_key = f"access_token:{access_token}"
        if redis_client.delete(access_key):
            logger.info(f"✅ Access token eliminado de Redis para user {current_user_id}")
        else:
            logger.warning(f"⚠ Access token no encontrado en Redis para user {current_user_id}")

        # Obtener y eliminar refresh token asociado
        refresh_key = f"access_to_refresh:{access_token}"
        refresh_token = redis_client.get(refresh_key)
        if refresh_token:
            refresh_token_key = f"refresh_token:{refresh_token}"
            if redis_client.delete(refresh_token_key):
                logger.info(f"✅ Refresh token eliminado de Redis para user {current_user_id}")
            redis_client.delete(refresh_key)  # Eliminar la relación

        logger.info(f"User logged out: {current_user_id}")

    except redis.ConnectionError as e:
        logger.error(f"Redis error during logout: {str(e)}")
        return jsonify({'message': 'Service temporarily unavailable'}), 503

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
    health_status = {
        'status': 'healthy',
        'database': 'connected',
        'redis': 'connected',
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    # Verificar base de datos
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            # Verificar también las tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            health_status['tables'] = [table['Tables_in_jwt_auth'] for table in tables]
            health_status['note'] = 'Tokens managed in Redis, not database'
        connection.close()
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status.update({
            'status': 'unhealthy',
            'database': 'disconnected',
            'database_error': str(e)
        })

    # Verificar Redis
    try:
        redis_client = get_redis_client()
        redis_client.ping()
        # Verificar algunas claves de tokens
        token_count = len(redis_client.keys('access_token:*'))
        health_status['redis_tokens'] = token_count
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        health_status.update({
            'status': 'unhealthy',
            'redis': 'disconnected',
            'redis_error': str(e)
        })

    status_code = 200 if health_status['status'] == 'healthy' else 500
    return jsonify(health_status), status_code

if __name__ == '__main__':
    logger.info("Iniciando microservicio JWT...")
    app.run(host='0.0.0.0', port=5000, debug=False)