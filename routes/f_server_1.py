from flask import Flask, jsonify, request
import requests
import hashlib
import shadow_crypt  # Rust library

app = Flask(__name__)

# Diffie-Hellman key exchange
@app.route('/diffie_hellman', methods=['GET'])
def diffie_hellman_route():

    private_key, public_key = shadow_crypt.generate_dh_key()
    response = requests.post('http://127.0.0.1:5001/receive_public_key', data=public_key)

    if response.status_code == 200:
        response_data = response.json()
        if 'server_public_key' in response_data:
            server_public_key = response_data['server_public_key']
            shared_key = shadow_crypt.derive_dh_shared_key(private_key, server_public_key)
            final_key = hashlib.sha256(shared_key.encode()).digest()

            return jsonify({
                'success': True,
                'server1_private_key': private_key,
                'server1_public_key': public_key,
                'server2_public_key': server_public_key,
                'final_key': final_key.hex()
            })
        else:
            return jsonify({'success': False, 'error': 'Server public key not found in response'})
    else:
        return jsonify({'success': False, 'error': f'Server 2 responded with status code {response.status_code}'})

# Elliptic Curve Diffie-Hellman key exchange
@app.route('/ecdh', methods=['GET'])
def ecdh_route():
    private_key, public_key = shadow_crypt.generate_ecdh_key()
    response = requests.post('http://127.0.0.1:5001/receive_public_key_ell_curve', data=public_key)

    if response.status_code == 200:
        response_data = response.json()
        if 'server_public_key' in response_data:
            server_public_key = bytes.fromhex(response_data['server_public_key'])
            shared_key = shadow_crypt.derive_ecdh_shared_key(private_key, server_public_key)
            final_key = hashlib.sha256(shared_key).digest()

            return jsonify({
                'success': True,
                'server1_private_key': private_key.hex(),
                'server1_public_key': public_key.hex(),
                'server2_public_key': response_data['server_public_key'],
                'final_key': final_key.hex()
            })
        else:
            return jsonify({'success': False, 'error': 'Server public key not found in response'})
    else:
        return jsonify({'success': False, 'error': f'Server 2 responded with status code {response.status_code}'})

# RSA encryption
@app.route('/rsa', methods=['POST'])
def rsa_route():
    private_key_rsa, public_key_rsa = shadow_crypt.generate_rsa_key()
    data = request.get_json()
    message = data['message']

    response = requests.post('http://127.0.0.1:5001/encrypt', json={
        'message': message,
        'public_key': public_key_rsa
    })

    if response.status_code == 200:
        encrypted_message = response.json()['encrypted_message']
        decrypted_message = shadow_crypt.rsa_decrypt(private_key_rsa, bytes.fromhex(encrypted_message))
        return jsonify({
            'success': True,
            'encrypted_message': encrypted_message,
            'decrypted_message': decrypted_message,
            'server1_public_key': public_key_rsa,
            'server1_private_key': private_key_rsa
        })
    else:
        return jsonify({'success': False, 'error': 'Encryption failed'})

# Crystals Kyber key encapsulation
@app.route('/kyber', methods=['GET'])
def kyber_route():
    public_key, secret_key = shadow_crypt.kyber_keygen()
    response = requests.post('http://127.0.0.1:5001/kyber_encapsulate', data=public_key)

    if response.status_code == 200:
        response_data = response.json()
        if 'ciphertext' in response_data:
            ciphertext = bytes.fromhex(response_data['ciphertext'])
            shared_secret = shadow_crypt.kyber_decapsulate(ciphertext, secret_key)

            return jsonify({
                'success': True,
                'server1_public_key': public_key.hex(),
                'server1_secret_key': secret_key.hex(),
                'server2_ciphertext': response_data['ciphertext'],
                'shared_secret': shared_secret.hex()
            })
        else:
            return jsonify({'success': False, 'error': 'Ciphertext not found in response'})
    else:
        return jsonify({'success': False, 'error': f'Server 2 responded with status code {response.status_code}'})

# NTRU Key Encapsulation Mechanism
@app.route('/ntru', methods=['GET'])
def ntru_route():
    # Generate NTRU key pair
    public_key, secret_key = shadow_crypt.ntru_generate_keypair()
    
    # Send public key to Server 2 for encapsulation
    response = requests.post('http://127.0.0.1:5001/ntru_encapsulate', data=public_key)

    if response.status_code == 200:
        response_data = response.json()
        
        if 'ciphertext' in response_data:
            ciphertext = bytes.fromhex(response_data['ciphertext'])
            
            # Decapsulate using the private key to retrieve the shared secret
            shared_secret = shadow_crypt.ntru_decapsulate(secret_key, ciphertext)
            final_key = hashlib.sha256(shared_secret).digest()

            return jsonify({
                'success': True,
                'server1_public_key': public_key.hex(),
                'server1_private_key': secret_key.hex(),
                'server2_ciphertext': response_data['ciphertext'],
                'shared_secret': shared_secret.hex(),
                'final_key': final_key.hex()
            })
        else:
            return jsonify({'success': False, 'error': 'Ciphertext not found in response'})
    else:
        return jsonify({'success': False, 'error': f'Server 2 responded with status code {response.status_code}'})


if __name__ == '__main__':
    app.run(port=5000, debug=True)