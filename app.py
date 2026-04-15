import os
import json
import time
import hashlib
import re
from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

app = Flask(__name__)

# Ensure required directories exist
os.makedirs("keys", exist_ok=True)
USERS_FILE = "users.json"
SIGNATURE_FILE = "signature.bin"
MESSAGE_FILE = "message.txt"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f).get("users", [])
    return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump({"users": users}, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/register", methods=["POST"])
def register():
    username = request.json.get("username", "").strip()
    if not username:
        return jsonify({"status": "error", "message": "Username cannot be empty"}), 400
    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        return jsonify({"status": "error", "message": "Invalid username format"}), 400
    
    users = load_users()
    if username in users:
        return jsonify({"status": "error", "message": "User already exists"}), 400
    
    users.append(username)
    save_users(users)
    return jsonify({"status": "success", "message": f"User '{username}' registered successfully"})

@app.route("/api/generate_keys", methods=["POST"])
def generate_keys():
    username = request.json.get("username", "").strip()
    users = load_users()
    if username not in users:
        return jsonify({"status": "error", "message": "User not registered"}), 400
    
    private_path = f"keys/{username}_private.pem"
    public_path = f"keys/{username}_public.pem"
    
    # Generate RSA keys
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    
    # Save keys
    with open(private_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    with open(public_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    # Get a preview of the public key
    with open(public_path, "r") as f:
        pub_preview = f.read().split('\n')[0:3] # First 3 lines
        pub_preview = '\n'.join(pub_preview) + '\n...'
        
    return jsonify({
        "status": "success", 
        "message": f"Keys generated successfully for '{username}'",
        "key_preview": pub_preview,
        "path": public_path
    })

@app.route("/api/sign", methods=["POST"])
def sign_message():
    username = request.json.get("username", "").strip()
    msg = request.json.get("message", "").strip()
    
    users = load_users()
    if username not in users:
        return jsonify({"status": "error", "message": "User not registered"}), 400
    
    private_path = f"keys/{username}_private.pem"
    if not os.path.exists(private_path):
        return jsonify({"status": "error", "message": "Keys not found for user"}), 400
    
    timestamp = str(int(time.time()))
    formatted_message = f"{username}:{msg}:{timestamp}".encode()
    hash_value = hashlib.sha256(formatted_message).hexdigest()
    
    with open(private_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    
    signature = private_key.sign(
        formatted_message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    
    with open(SIGNATURE_FILE, "wb") as f:
        f.write(signature)
    with open(MESSAGE_FILE, "wb") as f:
        f.write(formatted_message)
        
    return jsonify({
        "status": "success",
        "hash": hash_value,
        "payload": formatted_message.decode(),
        "signature_len": len(signature),
        "message": f"Message signed successfully by {username}"
    })

@app.route("/api/verify", methods=["POST"])
def verify_signature():
    username = request.json.get("username", "").strip()
    
    public_path = f"keys/{username}_public.pem"
    if not os.path.exists(public_path):
        return jsonify({"status": "error", "message": "No keys found for this user"}), 400
    
    if not os.path.exists(SIGNATURE_FILE) or not os.path.exists(MESSAGE_FILE):
        return jsonify({"status": "error", "message": "No signed message found"}), 400
    
    with open(public_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    
    with open(MESSAGE_FILE, "rb") as f:
        message = f.read()
    with open(SIGNATURE_FILE, "rb") as f:
        signature = f.read()
    
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        
        parts = message.decode().split(":")
        if parts[0] != username:
             return jsonify({"status": "error", "message": "Authentication Failed: Message does not belong to user"}), 400
             
        timestamp = int(parts[2])
        time_left = 60 - (int(time.time()) - timestamp)
        
        details = {
            "user_in_msg": parts[0],
            "timestamp": timestamp,
            "hash_algorithm": "SHA-256",
            "padding": "RSA-PSS",
            "valid_for": f"{time_left}s"
        }
        
        if time_left > 0:
            return jsonify({"status": "success", "message": "Authentication Successful", "details": details})
        else:
            return jsonify({"status": "error", "message": "Authentication Failed: Message Expired", "details": details}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Authentication Failed: Invalid Signature ({str(e)})"}), 400

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify({"users": load_users()})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
