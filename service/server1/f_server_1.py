from flask import Flask, jsonify, request
import requests
import hashlib
import shadow_crypt
import os

app = Flask(__name__)

SERVER2_URL = os.environ.get("SERVER2_URL", "http://localhost:5001")

# Health check for Render
@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

# Diffie-Hellman
@app.route('/diffie_hellman', methods=['GET'])
def diffie_hellman_route():
    # Generate key pair
    private_key1, public_key1 = shadow_crypt.generate_dh_key()
    public_key1_hex = bytes(public_key1).hex()
    
    # Callout server 2
    response = requests.post(f"{SERVER2_URL}/receive_public_key", data=public_key1_hex)
    if response.status_code != 200:
        return jsonify({'success': False, 'error': f'Server 2 error: {response.status_code}'}), response.status_code
    
    data = response.json()
    if 'server_public_key' not in data:
        return jsonify({'success': False, 'error': 'No public key received from Server 2'}), 500

    server_public_key = list(bytes.fromhex(data['server_public_key']))
    
    # Shared secret computation
    shared_key = shadow_crypt.derive_dh_shared_key(private_key1, server_public_key)
    final_key = hashlib.sha256(bytes(shared_key)).hexdigest()
    
    return jsonify({
        'success': True,
        'server1_private_key': bytes(private_key1).hex(),
        'server1_public_key': public_key1_hex,
        'server2_public_key': data['server_public_key'],
        'final_key': final_key
    })

# Elliptic Curve Diffie-Hellman
@app.route('/ecdh', methods=['GET'])
def ecdh_route():
    try:
        # Generate our own ECDH key pair
        private_key, public_key = shadow_crypt.generate_ecdh_key()
        public_key_hex = bytes(public_key).hex()
        
        # Callout server 2
        response = requests.post(f"{SERVER2_URL}/receive_public_key_ell_curve", data=public_key_hex)
        if response.status_code != 200:
            return jsonify({'success': False, 'error': f'Server 2 error: {response.status_code}'}), response.status_code
        
        res_json = response.json()
        if 'server_public_key' not in res_json:
            return jsonify({'success': False, 'error': 'No public key returned by Server 2'}), 500
        
        # Turn public key from hex string to bytes
        server_pub_hex = res_json['server_public_key']
        server_pub_bytes = bytes.fromhex(server_pub_hex)
        
        # Shared secret computation
        shared_key = shadow_crypt.derive_ecdh_shared_key(private_key, server_pub_bytes)
        final_key = hashlib.sha256(bytes(shared_key)).hexdigest()
        
        return jsonify({
            'success': True,
            'server1_private_key': bytes(private_key).hex(),
            'server1_public_key': public_key_hex,
            'server2_public_key': server_pub_hex,
            'final_key': final_key
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# RSA
@app.route('/rsa', methods=['POST'])
def rsa_route():
    try:
        # Generate RSA key pair
        rsa_private_key, rsa_public_key = shadow_crypt.generate_rsa_key()

        # Get the message from the incoming JSON payload
        data = request.get_json()
        message = data.get('message', "Hello, world!")

        # Send the public key and message to Server 2
        app.logger.info("Sending public key to Server 2 for encryption.")
        response = requests.post(f"{SERVER2_URL}/encrypt", json={
            'message': message,
            'public_key': rsa_public_key
        })
        app.logger.info("Received response from Server 2 with status code: %s", response.status_code)

        if response.status_code != 200:
            app.logger.error("Server 2 returned error status: %s", response.status_code)
            return jsonify({'success': False, 'error': f'Server 2 error: {response.status_code}'}), response.status_code

        res_json = response.json()
        app.logger.info("Response JSON from Server 2: %s", repr(res_json))
        if 'encrypted_message' not in res_json:
            app.logger.error("Encryption failed at Server 2: 'encrypted_message' key not found in response.")
            return jsonify({'success': False, 'error': 'Encryption failed at Server 2'}), 500

        # Convert the encrypted message from hex string back to bytes.
        encrypted_message_hex = res_json['encrypted_message']
        encrypted_message = bytes.fromhex(encrypted_message_hex)
        app.logger.info("Converted encrypted message from hex to bytes.")

        # Decrypt the encrypted message using our RSA private key.
        decrypted_message = shadow_crypt.rsa_decrypt(rsa_private_key, encrypted_message)
        app.logger.info("Decrypted message: %s", decrypted_message)

        return jsonify({
            'success': True,
            'encrypted_message': encrypted_message_hex,
            'decrypted_message': decrypted_message,
            'server1_public_key': rsa_public_key,
            'server1_private_key': rsa_private_key
        })
    except Exception as e:
        app.logger.exception("Exception occurred in rsa_route:")
        return jsonify({'success': False, 'error': str(e)}), 500

# Crystals Kyber
@app.route('/kyber', methods=['GET'])
def kyber_route():
    # Generate key pair
    kyber_public_key, kyber_secret_key = shadow_crypt.kyber_keygen()
    kyber_public_key_hex = kyber_public_key.hex() if isinstance(kyber_public_key, bytes) else str(kyber_public_key)

    # Send the public key and message to Server 2
    response = requests.post(f"{SERVER2_URL}/kyber_encapsulate", data=kyber_public_key_hex)
    if response.status_code != 200:
        return jsonify({'success': False, 'error': 'Error contacting Server 2'}), response.status_code
    resp = response.json()

    if 'ciphertext' not in resp:
        return jsonify({'success': False, 'error': 'Kyber encapsulation failed at Server 2'})
    ciphertext_hex = resp['ciphertext']

    # Decapsulation
    shared_secret = shadow_crypt.kyber_decapsulate(bytes.fromhex(ciphertext_hex), kyber_secret_key)
    return jsonify({
        'success': True,
        'server1_public_key': kyber_public_key_hex,
        'server1_secret_key': kyber_secret_key.hex() if isinstance(kyber_secret_key, bytes) else str(kyber_secret_key),
        'server2_ciphertext': ciphertext_hex,
        'shared_secret': shared_secret.hex() if isinstance(shared_secret, bytes) else str(shared_secret)
    })

# NTRU
@app.route('/ntru', methods=['GET'])
def ntru_route():
    # Generate key pair
    ntru_public_key, ntru_private_key = shadow_crypt.ntru_generate_keypair()

    ntru_public_key_hex = bytes(ntru_public_key).hex()
    ntru_private_key_hex = bytes(ntru_private_key).hex()
    
    # Send the public key to Server 2
    response = requests.post(f"{SERVER2_URL}/ntru_encapsulate", data=ntru_public_key_hex)
    if response.status_code != 200:
        return jsonify({'success': False, 'error': 'Error contacting Server 2'}), response.status_code
    
    resp = response.json()
    if 'ciphertext' not in resp:
        return jsonify({'success': False, 'error': 'NTRU encapsulation failed at Server 2'}), 500
    
    ciphertext_hex = resp['ciphertext']
    
    # Decapsulation
    shared_secret= shadow_crypt.ntru_decapsulate(bytes(ntru_private_key), bytes.fromhex(ciphertext_hex))
    final_key = hashlib.sha256(bytes(shared_secret)).hexdigest()
    
    return jsonify({
        'success': True,
        'server1_public_key': ntru_public_key_hex,
        'server1_private_key': ntru_private_key_hex,
        'server2_ciphertext': ciphertext_hex,
        'shared_secret': bytes(shared_secret).hex(),
        'final_key': final_key
    })

# Main
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
