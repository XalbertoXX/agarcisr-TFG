import shadow_crypt

def test_dh():
    print("\nTesting Diffie-Hellman key exchange...")
    private_key1, public_key1 = shadow_crypt.generate_dh_key()
    print(f"DH Private Key 1: {private_key1}")
    print(f"DH Public Key 1: {public_key1}")

    private_key2, public_key2 = shadow_crypt.generate_dh_key()
    print(f"DH Private Key 2: {private_key2}")
    print(f"DH Public Key 2: {public_key2}")

    shared_key1 = shadow_crypt.derive_dh_shared_key(private_key1, public_key2)
    shared_key2 = shadow_crypt.derive_dh_shared_key(private_key2, public_key1)

    print(f"DH Shared Key 1: {shared_key1}")
    print(f"DH Shared Key 2: {shared_key2}")

    assert shared_key1 == shared_key2, "Diffie-Hellman shared keys do not match!"
    print("Diffie-Hellman shared keys match!")

    print(f"Private key length: {len(private_key1)} bytes")
    print(f"Public key length: {len(public_key1)} bytes")
    print(f"Shared key length: {len(shared_key1)} bytes")

def test_ecdh():
    print("\nTesting ECDH key exchange...")
    ecdh_private_key, ecdh_public_key = shadow_crypt.generate_ecdh_key()
    print(f"ECDH Private Key: {ecdh_private_key}")
    print(f"ECDH Public Key: {ecdh_public_key}")

    ecdh_shared_key = shadow_crypt.derive_ecdh_shared_key(ecdh_private_key, ecdh_public_key)
    print(f"ECDH Shared Key: {ecdh_shared_key}")

def test_rsa():
    print("\nTesting RSA encryption/decryption...")
    rsa_private_key, rsa_public_key = shadow_crypt.generate_rsa_key()
    print(f"RSA Private Key: {rsa_private_key}")
    print(f"RSA Public Key: {rsa_public_key}")

    message = "Hello, world!"
    encrypted_message = shadow_crypt.rsa_encrypt(rsa_public_key, message)
    print(f"Encrypted Message: {encrypted_message}")

    decrypted_message = shadow_crypt.rsa_decrypt(rsa_private_key, encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")

def test_kyber():
    print("\nTesting Kyber key encapsulation...")
    kyber_public_key, kyber_secret_key = shadow_crypt.kyber_keygen()
    print(f"Kyber Public Key: {kyber_public_key.hex()}")
    print(f"Kyber Secret Key: {kyber_secret_key.hex()}")

    ciphertext, shared_secret_alice = shadow_crypt.kyber_encapsulate(kyber_public_key)
    print(f"Kyber Ciphertext: {ciphertext.hex()}")
    print(f"Kyber Shared Secret (Alice): {shared_secret_alice.hex()}")

    shared_secret_bob = shadow_crypt.kyber_decapsulate(ciphertext, kyber_secret_key)
    print(f"Kyber Shared Secret (Bob): {shared_secret_bob.hex()}")

    assert shared_secret_alice == shared_secret_bob, "Shared secrets do not match!"
    print("Kyber shared secrets match!")

# Function to test all Kyber operations together
def test_kyber_full_exchange():
    # Key pair
    public_key, secret_key = shadow_crypt.kyber_keygen()
    
    # Encapsulate
    ciphertext, shared_secret_alice = shadow_crypt.kyber_encapsulate(public_key)
    
    # Decapsulate
    shared_secret_bob = shadow_crypt.kyber_decapsulate(ciphertext, secret_key)
    
    # Verify
    if shared_secret_alice == shared_secret_bob:
        print("Kyber full exchange successful: shared secrets match!")
    else:
        print("Kyber full exchange failed: shared secrets do not match!")
        
def test_ntru():
    print("\nTesting NTRU key encapsulation...")
    ntru_public_key, ntru_private_key = shadow_crypt.ntru_generate_keypair()
    print(f"NTRU Public Key: {ntru_public_key}")
    print(f"NTRU Private Key: {ntru_private_key}")

    ciphertext, shared_secret_bob = shadow_crypt.ntru_encapsulate(ntru_public_key)
    print(f"NTRU Ciphertext: {ciphertext}")
    print(f"NTRU Shared Secret (Bob): {shared_secret_bob}")

    shared_secret_alice = shadow_crypt.ntru_decapsulate(ntru_private_key, ciphertext)
    print(f"NTRU Shared Secret (Alice): {shared_secret_alice}")

    assert shared_secret_alice == shared_secret_bob, "NTRU shared secrets do not match!"
    print("NTRU key encapsulation successful!")
    
def run_all_tests():
    test_dh()
    test_ecdh()
    test_rsa()
    test_kyber()
    test_kyber_full_exchange()
    test_ntru()

if __name__ == "__main__":
    run_all_tests()
