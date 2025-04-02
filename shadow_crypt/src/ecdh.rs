use pyo3::prelude::*;
use x25519_dalek::{StaticSecret, PublicKey};
use rand::rngs::OsRng;

// Elliptic Curve Diffie-Hellman key generation
#[pyfunction]
pub fn generate_ecdh_key() -> PyResult<(Vec<u8>, Vec<u8>)> {
    let private_key = StaticSecret::random_from_rng(OsRng);
    let public_key = PublicKey::from(&private_key);
    
    Ok((private_key.to_bytes().to_vec(), public_key.as_bytes().to_vec()))
}

// Elliptic Curve Diffie-Hellman key derivation
#[pyfunction]
pub fn derive_ecdh_shared_key(private_key_bytes: Vec<u8>, server_public_key_bytes: Vec<u8>) -> PyResult<Vec<u8>> {
    let private_key = StaticSecret::from(<[u8; 32]>::try_from(private_key_bytes.as_slice()).unwrap());
    let server_public_key = PublicKey::from(<[u8; 32]>::try_from(server_public_key_bytes.as_slice()).unwrap());

    let shared_secret = private_key.diffie_hellman(&server_public_key);
    Ok(shared_secret.as_bytes().to_vec())
}