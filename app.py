from flask import Flask, jsonify, request
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.backends import default_backend
import requests, secrets, numpy as np

app = Flask(__name__)

# Diffie-Hellman key exchange
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

# RSA encryption
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
        # Decrypt the message here for validation
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

# Generate prime number for Swoosh
def generate_prime_number(bits):
    return dh.generate_parameters(generator=2, key_size=bits, backend=default_backend()).p

# Generate matrix A for Swoosh (M-LWE based)
def generate_matrix_A(size, modulus):
    return np.random.randint(0, modulus, size=(size, size))

# Securely generate ternary noise
def generate_ternary_noise(size):
    return np.random.choice([-1, 0, 1], size=size)

# Swoosh key exchange
@app.route('/swoosh', methods=['POST'])
def swoosh_route():
    data = request.get_json()
    message = data['message'].encode()

    # Swoosh parameters
    q = generate_prime_number(12)  # Generate a 12-bit prime number dynamically
    d = secrets.randbelow(100) + 150  # Generate dimension dynamically, e.g., between 150 and 250
    size = secrets.randbelow(16) + 16  # Matrix size between 16 and 32

    # Generate matrix A
    A = generate_matrix_A(size, q)

    # Generate secret s and error e using secure random generation
    s1 = generate_ternary_noise(size)
    e1 = generate_ternary_noise(size)

    # Compute public key
    pk1 = (np.dot(s1, A) + e1) % q

    # Send public key to Server 2
    response = requests.post('http://127.0.0.1:5001/swoosh_receive', json={
        'public_key': pk1.tolist(),
        'modulus': q,
        'matrix_A': A.tolist()
    })

    if response.status_code == 200:
        response_data = response.json()
        pk2 = np.array(response_data['public_key'])
        e2 = generate_ternary_noise(size)

        # Compute shared key
        shared_key = (np.dot(s1, pk2) + np.dot(e1, e2)) % q

        # Derive final key
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'swoosh-key-exchange',
            backend=default_backend()
        ).derive(shared_key.tobytes())

        return jsonify({
            'success': True,
            'shared_key': derived_key.hex(),
            'server1_public_key': pk1.tolist(),
            'server1_secret_key': s1.tolist(),
            'server2_public_key': pk2.tolist()
        })
    else:
        return jsonify({'success': False, 'error': 'Key exchange failed'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)