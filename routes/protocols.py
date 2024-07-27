from flask import Flask, request, jsonify
import hashlib
import shadow_crypt  # Rust library created

app = Flask(__name__)

# Diffie-Hellman key exchange
@app.route('/receive_public_key', methods=['POST'])
def receive_public_key():
    try:
        # To be changed in next commits, just testing
        p = "85859950916484676125439334608092681304789214056884991689423104627417791485869"  # Example prime
        g = "2"   # Example generator
        public_key_from_server1 = request.data.decode()
        
        private_key, public_key = shadow_crypt.generate_dh_key(p, g)
        shared_key = shadow_crypt.derive_dh_shared_key(private_key, public_key_from_server1, p)
        final_key = hashlib.sha256(shared_key.encode()).digest()

        return jsonify({
            'success': True,
            'final_key': final_key.hex(),
            'server_public_key': public_key,
            'server2_private_key': private_key
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Key exchange failed: {str(e)}'})

# Elliptic Curve Diffie-Hellman key exchange
@app.route('/receive_public_key_ell_curve', methods=['POST'])
def receive_public_key_ell_curve():
    try:
        public_key_from_server1 = request.data
        
        private_key, public_key = shadow_crypt.generate_ecdh_key()
        shared_key = shadow_crypt.derive_ecdh_shared_key(private_key, public_key_from_server1)
        final_key = hashlib.sha256(shared_key).digest()

        return jsonify({
            'success': True,
            'final_key': final_key.hex(),
            'server_public_key': public_key.hex(),
            'server2_private_key': private_key.hex()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Key exchange failed: {str(e)}'})

# RSA Encryption
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    public_key = data['public_key']
    message = data['message']
    
    encrypted_message = shadow_crypt.rsa_encrypt(public_key, message)
    
    return jsonify({
        'encrypted_message': encrypted_message.hex(),
        'used_public_key': public_key
    })

# Swoosh NIKE receive public key and generate response
@app.route('/swoosh_receive', methods=['POST'])
def swoosh_receive_public_key():
    try:
        public_key_from_server1 = bytes.fromhex(request.data.decode('utf-8'))
        
        parameters = (2**14, 256, 32)
        private_key, public_key = shadow_crypt.swoosh_generate_keys(parameters)
        shared_key = shadow_crypt.swoosh_derive_shared_key(private_key, public_key_from_server1, parameters[0])
        final_key = hashlib.sha256(bytes(shared_key)).digest()

        return jsonify({
            'success': True,
            'final_key': final_key.hex(),
            'server_public_key': public_key.hex(),
            'server2_private_key': private_key.hex()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Key exchange failed: {str(e)}'})

# Crystals Kyber encapsulation
@app.route('/kyber_encapsulate', methods=['POST'])
def kyber_encapsulate():
    try:
        public_key = request.data
        
        ciphertext, shared_secret = shadow_crypt.kyber_encapsulate(public_key)

        return jsonify({
            'success': True,
            'ciphertext': ciphertext.hex(),
            'shared_secret': shared_secret.hex()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Kyber encapsulation failed: {str(e)}'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)