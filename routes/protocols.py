from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import numpy as np

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


# RSA Encryption
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

# Swoosh functions (to be implemented differently in the final version)
def swoosh_generate_parameters():
    return {'q': 2**14, 'd': 256, 'N': 32}

def swoosh_generate_keys(parameters):
    q, d, N = parameters['q'], parameters['d'], parameters['N']
    A = np.random.randint(0, q, size=(N, N))
    s = np.random.randint(-1, 2, size=N)
    e = np.random.randint(-1, 2, size=N)
    public_key = (np.dot(A, s) + e) % q
    return s, public_key

def swoosh_serialize_public_key(public_key):
    return public_key.tobytes()

def swoosh_deserialize_public_key(serialized_public_key):
    return np.frombuffer(serialized_public_key, dtype=int)

def swoosh_derive_shared_key(private_key, public_key):
    q = 2**14
    shared_key = (np.dot(private_key, public_key)) % q
    return shared_key.tobytes()

def swoosh_serialize_private_key(private_key):
    return private_key.tobytes()

# Swoosh NIKE receive public key and generate response
@app.route('/swoosh_receive', methods=['POST'])
def swoosh_receive_public_key():
    try:
        serialized_public_key_from_server1 = request.data
        public_key_from_server1 = swoosh_deserialize_public_key(serialized_public_key_from_server1)

        # Generate Swoosh keys
        parameters = swoosh_generate_parameters()
        private_key, public_key = swoosh_generate_keys(parameters)
        serialized_server_public_key = swoosh_serialize_public_key(public_key)

        # Derive the shared key
        shared_key = swoosh_derive_shared_key(private_key, public_key_from_server1)
        final_key = hashes.Hash(hashes.SHA256(), backend=default_backend())
        final_key.update(shared_key)
        final_key = final_key.finalize()

        # Return keys and shared secret
        return jsonify({
            'success': True,
            'final_key': final_key.hex(),
            'server_public_key': serialized_server_public_key.hex(),
            'server2_private_key': swoosh_serialize_private_key(private_key).hex()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Key exchange failed: {str(e)}'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)