from flask import Flask, request, jsonify
import hashlib
import shadow_crypt

app = Flask(__name__)

# Health check for Render
@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

# Diffie-Hellman
@app.route('/receive_public_key', methods=['POST'])
def receive_public_key():
    try:
        # Receive public key 
        public_key_from_server1 = list(bytes.fromhex(request.data.decode()))
        
        # Generate key pair
        private_key2, public_key2 = shadow_crypt.generate_dh_key()
        shared_key = shadow_crypt.derive_dh_shared_key(private_key2, public_key_from_server1)
        final_key = hashlib.sha256(bytes(shared_key)).hexdigest()
        
        server_public_key_hex = bytes(public_key2).hex()
        server_private_key_hex = bytes(private_key2).hex()
        
        return jsonify({
            'success': True,
            'final_key': final_key,
            'server_public_key': server_public_key_hex,
            'server2_private_key': server_private_key_hex
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Key exchange failed: {str(e)}'})

# Elliptic Curve Diffie-Hellman
@app.route('/receive_public_key_ell_curve', methods=['POST'])
def receive_public_key_ell_curve():
    try:
        # Receive public key
        client_pub_hex = request.data.decode()
        client_pub_bytes = bytes.fromhex(client_pub_hex)
        
        # Generate key pair.
        private_key, public_key = shadow_crypt.generate_ecdh_key()
        shared_key = shadow_crypt.derive_ecdh_shared_key(private_key, client_pub_bytes)
        final_key = hashlib.sha256(bytes(shared_key)).hexdigest()
        
        # Convert our public key (list of ints) to bytes then hex string.
        server_public_key_hex = bytes(public_key).hex()
        server_private_key_hex = bytes(private_key).hex()
        
        return jsonify({
            'success': True,
            'final_key': final_key,
            'server_public_key': server_public_key_hex,
            'server2_private_key': server_private_key_hex
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# RSA 
@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        # Get the encrypted message
        data = request.get_json()
        public_key = data['public_key']
        message = data['message']

        encrypted_message_list = shadow_crypt.rsa_encrypt(public_key, message)
        encrypted_message_bytes = bytes(encrypted_message_list)
        
        return jsonify({
            'encrypted_message': encrypted_message_bytes.hex(),
            'used_public_key': public_key
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Crystals Kyber
@app.route('/kyber_encapsulate', methods=['POST'])
def kyber_encapsulate():
    try:
        # Expect public key
        public_key_hex = request.data.decode()
        public_key = bytes.fromhex(public_key_hex)
        ciphertext, shared_secret = shadow_crypt.kyber_encapsulate(public_key)
        return jsonify({
            'success': True,
            'ciphertext': ciphertext.hex(),
            'shared_secret': shared_secret.hex()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# NTRU
@app.route('/ntru_encapsulate', methods=['POST'])
def ntru_encapsulate():
    try:
        # Expect the public key from Server 1 
        public_key_hex = request.data.decode()
        public_key = bytes.fromhex(public_key_hex)
        
        # Perform encapsulation
        ciphertext, shared_secret = shadow_crypt.ntru_encapsulate(public_key)
        
        return jsonify({
            'success': True,
            'ciphertext': bytes(ciphertext).hex(),
            'shared_secret': bytes(shared_secret).hex()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Main
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)