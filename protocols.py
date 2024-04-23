from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

@app.route('/receive_public_key', methods=['POST'])
def receive_public_key():
    try:
        serialized_public_key_from_server1 = request.data
        public_key_from_server1 = serialization.load_der_public_key(serialized_public_key_from_server1, backend=default_backend())

        # Use the parameters from Server 1's public key
        parameters = public_key_from_server1.parameters()
        private_key = parameters.generate_private_key()
        server_public_key = private_key.public_key()
        serialized_server_public_key = server_public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        shared_key = private_key.exchange(public_key_from_server1)
        derived_key = hashes.Hash(hashes.SHA256(), backend=default_backend())
        derived_key.update(shared_key)
        final_key = derived_key.finalize()

        # Return private key and public keys
        return jsonify({
            'success': True, 
            'final_key': final_key.hex(),
            'server_public_key': serialized_server_public_key.hex(),
            'server2_private_key': private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).hex()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Key exchange failed: {str(e)}'})

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    public_key_data = bytes.fromhex(data['public_key'])
    message = bytes.fromhex(data['message'])

    public_key = serialization.load_pem_public_key(public_key_data, backend=default_backend())

    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    return jsonify({
        'encrypted_message': encrypted_message.hex(),
        'used_public_key': public_key_data.hex()
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)