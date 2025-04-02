use pyo3::prelude::*;
use rsa::{RsaPrivateKey, RsaPublicKey, Pkcs1v15Encrypt};
use rsa::pkcs1::{DecodeRsaPrivateKey, DecodeRsaPublicKey, EncodeRsaPrivateKey, EncodeRsaPublicKey};
use rsa::pkcs8::LineEnding;
use rand::rngs::OsRng;

// RSA key generation
#[pyfunction]
pub fn generate_rsa_key() -> (String, String) {
    let mut rng = OsRng;
    let bits = 2048;

    let private_key = RsaPrivateKey::new(&mut rng, bits).unwrap();
    let public_key = RsaPublicKey::from(&private_key);

    let private_pem = private_key.to_pkcs1_pem(LineEnding::LF).unwrap();
    let public_pem = public_key.to_pkcs1_pem(LineEnding::LF).unwrap();

    (private_pem.to_string(), public_pem)
}

// RSA encryption
#[pyfunction]
pub fn rsa_encrypt(public_key_pem: &str, message: &str) -> Vec<u8> {
    let public_key = RsaPublicKey::from_pkcs1_pem(public_key_pem).unwrap();
    let mut rng = OsRng;
    public_key.encrypt(&mut rng, Pkcs1v15Encrypt, message.as_bytes()).unwrap()
}

// RSA decryption
#[pyfunction]
pub fn rsa_decrypt(private_key_pem: &str, encrypted_data: Vec<u8>) -> String {
    let private_key = RsaPrivateKey::from_pkcs1_pem(private_key_pem).unwrap();
    let decrypted_data = private_key.decrypt(Pkcs1v15Encrypt, &encrypted_data).unwrap();
    String::from_utf8(decrypted_data).unwrap()
}