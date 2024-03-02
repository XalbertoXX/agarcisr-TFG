from flask import Flask, jsonify
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh
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

            except Exception as e:
                return jsonify({'success': False, 'error': f'Error during key exchange: {str(e)}'})
        else:
            return jsonify({'success': False, 'error': 'Server public key not found in response'})
    else:
        return jsonify({'success': False, 'error': f'Server 2 responded with status code {response.status_code}'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
