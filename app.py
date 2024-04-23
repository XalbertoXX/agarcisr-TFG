from flask import Flask, jsonify, request
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.backends import default_backend
import requests

app = Flask(__name__)

@app.route('/diffie_hellman', methods=['GET'])
def diffie_hellman_route():
    # Generate Diffie-Hellman parameters and keys
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()

    # Serialize public key and send to Server 2
    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    response = requests.post('http://127.0.0.1:5001/receive_public_key', data=serialized_public_key)

    if response.status_code == 200:
        response_data = response.json()
        if 'server_public_key' in response_data:
            try:
                server_public_key = serialization.load_der_public_key(
                    bytes.fromhex(response_data['server_public_key']), 
                    backend=default_backend()
                )

                # Perform key exchange
                shared_key = private_key.exchange(server_public_key)
                derived_key = hashes.Hash(hashes.SHA256(), backend=default_backend())
                derived_key.update(shared_key)
                final_key = derived_key.finalize()

                # Return private key and public keys
                return jsonify({
                    'success': True, 
                    'server1_private_key': private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    ).hex(),
                    'server1_public_key': serialized_public_key.hex(),
                    'server2_public_key': response_data['server_public_key'],
                    'final_key': final_key.hex()
                })
            except Exception as e:
                return jsonify({'success': False, 'error': f'Error during key exchange: {str(e)}'})
        else:
            return jsonify({'success': False, 'error': 'Server public key not found in response'})
    else:
        return jsonify({'success': False, 'error': f'Server 2 responded with status code {response.status_code}'})


@app.route('/rsa', methods=['POST'])
def rsa_route():

    # Generate RSA keys inside the function
    private_key_rsa = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key_rsa = private_key_rsa.public_key()
    serialized_public_key_rsa = public_key_rsa.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    data = request.get_json()
    message = data['message'].encode()

    # Send message and public key to protocols.py for encryption
    response = requests.post('http://127.0.0.1:5001/encrypt', json={
        'message': message.hex(),
        'public_key': serialized_public_key_rsa.hex()
    })

    if response.status_code == 200:
        encrypted_message = response.json()['encrypted_message']
        # Optionally, decrypt the message here for validation
        decrypted_message = private_key_rsa.decrypt(
            bytes.fromhex(encrypted_message),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        return jsonify({
            'success': True,
            'encrypted_message': encrypted_message,
            'decrypted_message': decrypted_message.decode(),
            'server1_public_key': serialized_public_key_rsa.hex(),
            'server1_private_key': private_key_rsa.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).hex()
        })
    else:
        return jsonify({'success': False, 'error': 'Encryption failed'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)