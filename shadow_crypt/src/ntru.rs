use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use ntrust_native::{
    AesState,
    RNGState,
    crypto_kem_dec,
    crypto_kem_enc,
    crypto_kem_keypair,
    CRYPTO_PUBLICKEYBYTES,
    CRYPTO_SECRETKEYBYTES,
    CRYPTO_CIPHERTEXTBYTES,
    CRYPTO_BYTES,
};
use rand::RngCore;

// AesState initialize
fn seeded_rng() -> Result<AesState, String> {
    let mut entropy_input = [0u8; 48];
    rand::rngs::OsRng.fill_bytes(&mut entropy_input);
    let mut rng_instance = AesState::new();
    rng_instance.randombytes_init(entropy_input);

    Ok(rng_instance)
}

// NTRU key generation
#[pyfunction]
pub fn ntru_generate_keypair() -> PyResult<(Vec<u8>, Vec<u8>)> {
    let mut rng = seeded_rng().map_err(|e_str| PyValueError::new_err(format!("RNG initialization failed: {}", e_str)))?;
    let mut pk = [0u8; CRYPTO_PUBLICKEYBYTES];
    let mut sk = [0u8; CRYPTO_SECRETKEYBYTES];

    crypto_kem_keypair(&mut pk, &mut sk, &mut rng).map_err(|e| PyValueError::new_err(format!("Failed to generate key pair: {:?}", e)))?;

    Ok((pk.to_vec(), sk.to_vec()))
}

// NTRU key encryption
#[pyfunction]
pub fn ntru_encapsulate(public_key: &[u8]) -> PyResult<(Vec<u8>, Vec<u8>)> {

    if public_key.len() != CRYPTO_PUBLICKEYBYTES {return Err(PyValueError::new_err("Invalid public key length"));}

    let mut rng = seeded_rng().map_err(|e_str| PyValueError::new_err(format!("RNG initialization failed: {}", e_str)))?;
    let mut ct = [0u8; CRYPTO_CIPHERTEXTBYTES];
    let mut ss = [0u8; CRYPTO_BYTES];
    let pk_array: [u8; CRYPTO_PUBLICKEYBYTES] = public_key.try_into().map_err(|_| PyValueError::new_err("Failed to convert public key"))?;
    crypto_kem_enc(&mut ct, &mut ss, &pk_array, &mut rng).map_err(|e| PyValueError::new_err(format!("Encryption failed: {:?}", e)))?;

    Ok((ct.to_vec(), ss.to_vec()))
}

// NTRU key decryption
#[pyfunction]
pub fn ntru_decapsulate(private_key: &[u8], ciphertext: &[u8]) -> PyResult<Vec<u8>> {
    if private_key.len() != CRYPTO_SECRETKEYBYTES {return Err(PyValueError::new_err("Invalid private key length"));}
    if ciphertext.len() != CRYPTO_CIPHERTEXTBYTES {return Err(PyValueError::new_err("Invalid ciphertext length"));}

    let mut ss = [0u8; CRYPTO_BYTES];
    let sk_array: [u8; CRYPTO_SECRETKEYBYTES] = private_key.try_into().map_err(|_| PyValueError::new_err("Failed to convert private key"))?;
    let ct_array: [u8; CRYPTO_CIPHERTEXTBYTES] = ciphertext.try_into().map_err(|_| PyValueError::new_err("Failed to convert ciphertext"))?;
    crypto_kem_dec(&mut ss, &ct_array, &sk_array).map_err(|e| PyValueError::new_err(format!("Decryption failed: {:?}", e)))?;

    Ok(ss.to_vec())
}