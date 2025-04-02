use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use ntrust_native::{
    AesState,
    crypto_kem_dec,
    crypto_kem_enc,
    crypto_kem_keypair,
    CRYPTO_PUBLICKEYBYTES,
    CRYPTO_SECRETKEYBYTES,
    CRYPTO_CIPHERTEXTBYTES,
    CRYPTO_BYTES,
};

// NTRU key generation
pub fn generate_ntru_keys() -> PyResult<(Vec<u8>, Vec<u8>)> {
    let mut rng = AesState::new();
    let mut pk = [0u8; CRYPTO_PUBLICKEYBYTES];
    let mut sk = [0u8; CRYPTO_SECRETKEYBYTES];

    crypto_kem_keypair(&mut pk, &mut sk, &mut rng)
        .map_err(|e| PyValueError::new_err(format!("Failed to generate key pair: {:?}", e)))?;

    Ok((pk.to_vec(), sk.to_vec()))
}

// NTRU key ecnryption
pub fn ntru_encrypt(public_key: &[u8]) -> PyResult<(Vec<u8>, Vec<u8>)> {
    if public_key.len() != CRYPTO_PUBLICKEYBYTES {
        return Err(PyValueError::new_err("Invalid public key length"));
    }

    let mut rng = AesState::new();
    let mut ct = [0u8; CRYPTO_CIPHERTEXTBYTES];
    let mut ss = [0u8; CRYPTO_BYTES];

    let pk: [u8; CRYPTO_PUBLICKEYBYTES] = public_key.try_into()
        .map_err(|_| PyValueError::new_err("Failed to convert public key"))?;

    crypto_kem_enc(&mut ct, &mut ss, &pk, &mut rng)
        .map_err(|e| PyValueError::new_err(format!("Encryption failed: {:?}", e)))?;

    Ok((ct.to_vec(), ss.to_vec()))
}

// NTRU key decryption
pub fn ntru_decrypt(private_key: &[u8], ciphertext: &[u8]) -> PyResult<Vec<u8>> {
    if private_key.len() != CRYPTO_SECRETKEYBYTES {
        return Err(PyValueError::new_err("Invalid private key length"));
    }
    if ciphertext.len() != CRYPTO_CIPHERTEXTBYTES {
        return Err(PyValueError::new_err("Invalid ciphertext length"));
    }

    let mut ss = [0u8; CRYPTO_BYTES];

    let sk: [u8; CRYPTO_SECRETKEYBYTES] = private_key.try_into()
        .map_err(|_| PyValueError::new_err("Failed to convert private key"))?;
    let ct: [u8; CRYPTO_CIPHERTEXTBYTES] = ciphertext.try_into()
        .map_err(|_| PyValueError::new_err("Failed to convert ciphertext"))?;

    crypto_kem_dec(&mut ss, &ct, &sk)
        .map_err(|e| PyValueError::new_err(format!("Decryption failed: {:?}", e)))?;

    Ok(ss.to_vec())
}

#[pyfunction]
pub fn ntru_generate_keypair() -> PyResult<(Vec<u8>, Vec<u8>)> {
    generate_ntru_keys()
}

#[pyfunction]
pub fn ntru_encapsulate(public_key: Vec<u8>) -> PyResult<(Vec<u8>, Vec<u8>)> {
    ntru_encrypt(&public_key)
}

#[pyfunction]
pub fn ntru_decapsulate(private_key: Vec<u8>, ciphertext: Vec<u8>) -> PyResult<Vec<u8>> {
    ntru_decrypt(&private_key, &ciphertext)
}