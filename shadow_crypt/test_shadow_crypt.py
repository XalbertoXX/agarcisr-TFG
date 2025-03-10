import shadow_crypt

# Test the Diffie-Hellman key exchange.
def test_dh():
    # Kick things off: we're checking the Diffie-Hellman key exchange.
    print("\nTesting Diffie-Hellman key exchange...")
    
    # Generate the first key pair.
    private_key1, public_key1 = shadow_crypt.generate_dh_key()
    print(f"DH Private Key 1: {private_key1}")
    print(f"DH Public Key 1: {public_key1}")

    # Generate a second key pair.
    private_key2, public_key2 = shadow_crypt.generate_dh_key()
    print(f"DH Private Key 2: {private_key2}")
    print(f"DH Public Key 2: {public_key2}")

    # Each party computes the shared key using the other's public key.
    shared_key1 = shadow_crypt.derive_dh_shared_key(private_key1, public_key2)
    shared_key2 = shadow_crypt.derive_dh_shared_key(private_key2, public_key1)

    # Print the shared keys to see if they match.
    print(f"DH Shared Key 1: {shared_key1}")
    print(f"DH Shared Key 2: {shared_key2}")

    # Assert that both shared keys are identical.
    assert shared_key1 == shared_key2, "Diffie-Hellman shared keys do not match!"
    print("Diffie-Hellman shared keys match!")

    # Extra info: output the length of keys (helpful for sanity checks).
    print(f"Private key length: {len(private_key1)} bytes")
    print(f"Public key length: {len(public_key1)} bytes")
    print(f"Shared key length: {len(shared_key1)} bytes")

# Test the Elliptic Curve Diffie-Hellman (ECDH) key exchange.
def test_ecdh():
    print("\nTesting ECDH key exchange...")
    # Generate the ECDH key pair.
    ecdh_private_key, ecdh_public_key = shadow_crypt.generate_ecdh_key()
    print(f"ECDH Private Key: {ecdh_private_key}")
    print(f"ECDH Public Key: {ecdh_public_key}")

    # Compute the shared key using the same key pair.
    ecdh_shared_key = shadow_crypt.derive_ecdh_shared_key(ecdh_private_key, ecdh_public_key)
    print(f"ECDH Shared Key: {ecdh_shared_key}")

# Test RSA encryption and decryption.
def test_rsa():
    print("\nTesting RSA encryption/decryption...")
    # Generate an RSA key pair.
    rsa_private_key, rsa_public_key = shadow_crypt.generate_rsa_key()
    print(f"RSA Private Key: {rsa_private_key}")
    print(f"RSA Public Key: {rsa_public_key}")

    # Define a simple message to encrypt.
    message = "Hello, world!"
    # Encrypt the message using the public key.
    encrypted_message = shadow_crypt.rsa_encrypt(rsa_public_key, message)
    print(f"Encrypted Message: {encrypted_message}")

    # Decrypt the encrypted message with the private key.
    decrypted_message = shadow_crypt.rsa_decrypt(rsa_private_key, encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")

# Test the Kyber key encapsulation mechanism (KEM).
def test_kyber():
    print("\nTesting Kyber key encapsulation...")
    # Generate the Kyber key pair.
    kyber_public_key, kyber_secret_key = shadow_crypt.kyber_keygen()
    print(f"Kyber Public Key: {kyber_public_key.hex()}")
    print(f"Kyber Secret Key: {kyber_secret_key.hex()}")

    # Encapsulate a shared secret using the public key.
    ciphertext, shared_secret_alice = shadow_crypt.kyber_encapsulate(kyber_public_key)
    print(f"Kyber Ciphertext: {ciphertext.hex()}")
    print(f"Kyber Shared Secret (Alice): {shared_secret_alice.hex()}")

    # Decapsulate the shared secret with the secret key.
    shared_secret_bob = shadow_crypt.kyber_decapsulate(ciphertext, kyber_secret_key)
    print(f"Kyber Shared Secret (Bob): {shared_secret_bob.hex()}")

    # Ensure both shared secrets match.
    assert shared_secret_alice == shared_secret_bob, "Shared secrets do not match!"
    print("Kyber shared secrets match!")

# Perform a full Kyber key exchange test.
def test_kyber_full_exchange():
    # Generate a new key pair for Kyber.
    public_key, secret_key = shadow_crypt.kyber_keygen()
    
    # Use the public key to encapsulate a shared secret.
    ciphertext, shared_secret_alice = shadow_crypt.kyber_encapsulate(public_key)
    
    # Use the secret key to recover the shared secret.
    shared_secret_bob = shadow_crypt.kyber_decapsulate(ciphertext, secret_key)
    
    # Check that both parties arrived at the same secret.
    if shared_secret_alice == shared_secret_bob:
        print("Kyber full exchange successful: shared secrets match!")
    else:
        print("Kyber full exchange failed: shared secrets do not match!")
        
# Test the NTRU key encapsulation mechanism.
def test_ntru():
    print("\nTesting NTRU key encapsulation...")
    # Generate an NTRU key pair.
    ntru_public_key, ntru_private_key = shadow_crypt.ntru_generate_keypair()
    print(f"NTRU Public Key: {ntru_public_key}")
    print(f"NTRU Private Key: {ntru_private_key}")

    # Encapsulate a shared secret using the NTRU public key.
    ciphertext, shared_secret_bob = shadow_crypt.ntru_encapsulate(ntru_public_key)
    print(f"NTRU Ciphertext: {ciphertext}")
    print(f"NTRU Shared Secret (Bob): {shared_secret_bob}")

    # Decapsulate to obtain the shared secret with the private key.
    shared_secret_alice = shadow_crypt.ntru_decapsulate(ntru_private_key, ciphertext)
    print(f"NTRU Shared Secret (Alice): {shared_secret_alice}")

    # Confirm that both shared secrets are the same.
    assert shared_secret_alice == shared_secret_bob, "NTRU shared secrets do not match!"
    print("NTRU key encapsulation successful!")
    
# Run all the tests in sequence.
def run_all_tests():
    test_dh()
    test_ecdh()
    test_rsa()
    test_kyber()
    test_kyber_full_exchange()
    test_ntru()

# When this script is executed directly, run all the tests.
if __name__ == "__main__":
    run_all_tests()