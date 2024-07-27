import shadow_crypt

# Test Diffie-Hellman key generation
p = "23"
g = "5"
private_key, public_key = shadow_crypt.generate_dh_key(p, g)
print(f"DH Private Key: {private_key}")
print(f"DH Public Key: {public_key}")

# Test deriving shared key
server_public_key = public_key  # Assuming server public key is the same for the test
shared_key = shadow_crypt.derive_dh_shared_key(private_key, server_public_key, p)
print(f"DH Shared Key: {shared_key}")

# Test ECDH key generation
ecdh_private_key, ecdh_public_key = shadow_crypt.generate_ecdh_key()
print(f"ECDH Private Key: {ecdh_private_key}")
print(f"ECDH Public Key: {ecdh_public_key}")

# Test deriving ECDH shared key
ecdh_shared_key = shadow_crypt.derive_ecdh_shared_key(ecdh_private_key, ecdh_public_key)
print(f"ECDH Shared Key: {ecdh_shared_key}")

# Test RSA key generation
rsa_private_key, rsa_public_key = shadow_crypt.generate_rsa_key()
print(f"RSA Private Key: {rsa_private_key}")
print(f"RSA Public Key: {rsa_public_key}")

# Test RSA encryption/decryption
message = "Hello, world!"
encrypted_message = shadow_crypt.rsa_encrypt(rsa_public_key, message)
print(f"Encrypted Message: {encrypted_message}")

decrypted_message = shadow_crypt.rsa_decrypt(rsa_private_key, encrypted_message)
print(f"Decrypted Message: {decrypted_message}")

# Test Swoosh key generation
swoosh_private_key, swoosh_public_key = shadow_crypt.swoosh_generate_keys((23, 0, 5))
print(f"Swoosh Private Key: {swoosh_private_key}")
print(f"Swoosh Public Key: {swoosh_public_key}")

# Test deriving Swoosh shared key
swoosh_shared_key = shadow_crypt.swoosh_derive_shared_key(swoosh_private_key, swoosh_public_key, 23)
print(f"Swoosh Shared Key: {swoosh_shared_key}")

# Test Kyber key generation
kyber_public_key, kyber_secret_key = shadow_crypt.kyber_keygen()
print(f"Kyber Public Key: {kyber_public_key.hex()}")
print(f"Kyber Secret Key: {kyber_secret_key.hex()}")

# Test Kyber encapsulation
ciphertext, shared_secret_alice = shadow_crypt.kyber_encapsulate(kyber_public_key)
print(f"Kyber Ciphertext: {ciphertext.hex()}")
print(f"Kyber Shared Secret (Alice): {shared_secret_alice.hex()}")

# Test Kyber decapsulation
shared_secret_bob = shadow_crypt.kyber_decapsulate(ciphertext, kyber_secret_key)
print(f"Kyber Shared Secret (Bob): {shared_secret_bob.hex()}")

# Verify that both parties share the same secret
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

test_kyber_full_exchange()
