import os
import boto3
import jwt
import datetime
from flask import Flask, request, jsonify, render_template
from functools import wraps
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Initialize S3 Client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# --- CORS Configuration ---
def apply_s3_cors():
    """
    Applies CORS policy to the S3 bucket to allow localhost access.
    Run this once on application startup.
    """
    print(f"Configuring CORS for bucket: {BUCKET_NAME}...")
    try:
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
                'AllowedOrigins': ['http://127.0.0.1:5000'], # Adjust for production
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3000
            }]
        }
        s3_client.put_bucket_cors(Bucket=BUCKET_NAME, CORSConfiguration=cors_configuration)
        print("✅ CORS configuration applied successfully.")
    except Exception as e:
        print(f"❌ Failed to configure CORS: {e}")

# Hardcoded Users (for demonstration)
USERS = {
    "admin": "password123",
    "user": "userpass"
}

# --- Middleware / Decorators ---

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic realm="Login required!"'}), 401

    user = auth.get('username')
    password = auth.get('password')

    if user in USERS and USERS[user] == password:
        token = jwt.encode({
            'user': user,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic realm="Login required!"'}), 401

@app.route('/api/upload-url', methods=['POST'])
@token_required
def create_upload_url(current_user):
    """Generates a Presigned URL for PUT (Upload)"""
    data = request.json
    filename = data.get('filename')
    file_type = data.get('fileType')
    
    if not filename:
        return jsonify({'message': 'Filename is required'}), 400

    # Create a unique key for the file
    key = f"user-profile-images/{current_user}/{filename}"

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key,
                'ContentType': file_type
            },
            ExpiresIn=300  # 5 minutes
        )
        return jsonify({'uploadUrl': url, 'fileKey': key})
    except ClientError as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/read-url', methods=['GET'])
@token_required
def create_read_url(current_user):
    """Generates a Presigned URL for GET (Read)"""
    key = request.args.get('key')
    
    if not key:
        return jsonify({'message': 'File key is required'}), 400

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key
            },
            ExpiresIn=3600  # 1 hour
        )
        return jsonify({'readUrl': url})
    except ClientError as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/save-profile', methods=['POST'])
@token_required
def save_profile(current_user):
    """Save user's profile image key to JSON file"""
    data = request.json
    file_key = data.get('fileKey')
    
    if not file_key:
        return jsonify({'message': 'fileKey is required'}), 400
    
    try:
        import json
        store_path = 'user_profiles.json'
        profiles = {}
        
        # Load existing profiles if file exists
        if os.path.exists(store_path):
            with open(store_path) as f:
                profiles = json.load(f)
        
        # Update current user's profile
        profiles[current_user] = file_key
        
        # Save back to file
        with open(store_path, 'w') as f:
            json.dump(profiles, f, indent=2)
        
        return jsonify({'message': 'Profile saved successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/me', methods=['GET'])
@token_required
def get_me(current_user):
    """Get current user profile info"""
    file_key = None
    try:
        import json
        store_path = 'user_profiles.json'
        if os.path.exists(store_path):
            with open(store_path) as f:
                profiles = json.load(f)
            file_key = profiles.get(current_user)
    except Exception:
        pass
    
    return jsonify({
        'username': current_user,
        'fileKey': file_key
    })

if __name__ == '__main__':
    apply_s3_cors()
    app.run(debug=True)
