use pyo3::prelude::*;
use pyo3::types::PyBytes;
use pyo3::wrap_pyfunction;
use x25519_dalek::{StaticSecret, PublicKey};
use rand::Rng;
use rand::rngs::OsRng;
use num_bigint::{BigUint, RandBigInt};
use rsa::{RsaPrivateKey, RsaPublicKey, Pkcs1v15Encrypt};
use rsa::pkcs1::{DecodeRsaPrivateKey, DecodeRsaPublicKey, EncodeRsaPrivateKey, EncodeRsaPublicKey};
use rsa::pkcs8::LineEnding;
use kyberlib::*;

// diffie_hellman constants
const DH_PRIME: &str = "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF";
const DH_GENERATOR: u32 = 2;

#[pyfunction]
fn generate_dh_key() -> PyResult<(Vec<u8>, Vec<u8>)> {
    let p = BigUint::parse_bytes(DH_PRIME.as_bytes(), 16).unwrap();
    let g = BigUint::from(DH_GENERATOR);

    let mut rng = rand::thread_rng();
    let private_key = rng.gen_biguint_range(&BigUint::from(2u32), &p);
    let public_key = g.modpow(&private_key, &p);

    Ok((private_key.to_bytes_be().to_vec(), public_key.to_bytes_be().to_vec()))
}

#[pyfunction]
fn derive_dh_shared_key(private_key: Vec<u8>, other_public_key: Vec<u8>) -> PyResult<Vec<u8>> {
    let p = BigUint::parse_bytes(DH_PRIME.as_bytes(), 16).unwrap();
    let private_key = BigUint::from_bytes_be(&private_key);
    let other_public_key = BigUint::from_bytes_be(&other_public_key);

    let shared_secret = other_public_key.modpow(&private_key, &p);
    Ok(shared_secret.to_bytes_be().to_vec())
}

// Elliptic Curve Diffie-Hellman
#[pyfunction]
fn generate_ecdh_key() -> PyResult<(Vec<u8>, Vec<u8>)> {
    let private_key = StaticSecret::random_from_rng(OsRng);
    let public_key = PublicKey::from(&private_key);
    
    Ok((private_key.to_bytes().to_vec(), public_key.as_bytes().to_vec()))
}

#[pyfunction]
fn derive_ecdh_shared_key(private_key_bytes: Vec<u8>, server_public_key_bytes: Vec<u8>) -> PyResult<Vec<u8>> {
    let private_key = StaticSecret::from(<[u8; 32]>::try_from(private_key_bytes.as_slice()).unwrap());
    let server_public_key = PublicKey::from(<[u8; 32]>::try_from(server_public_key_bytes.as_slice()).unwrap());

    let shared_secret = private_key.diffie_hellman(&server_public_key);
    Ok(shared_secret.as_bytes().to_vec())
}

// RSA Functions
#[pyfunction]
fn generate_rsa_key() -> (String, String) {
    let mut rng = OsRng;
    let bits = 2048;

    let private_key = RsaPrivateKey::new(&mut rng, bits).unwrap();
    let public_key = RsaPublicKey::from(&private_key);

    let private_pem = private_key.to_pkcs1_pem(LineEnding::LF).unwrap();
    let public_pem = public_key.to_pkcs1_pem(LineEnding::LF).unwrap();

    (private_pem.to_string(), public_pem)
}

#[pyfunction]
fn rsa_encrypt(public_key_pem: &str, message: &str) -> Vec<u8> {
    let public_key = RsaPublicKey::from_pkcs1_pem(public_key_pem).unwrap();
    let mut rng = OsRng;
    public_key.encrypt(&mut rng, Pkcs1v15Encrypt, message.as_bytes()).unwrap()
}

#[pyfunction]
fn rsa_decrypt(private_key_pem: &str, encrypted_data: Vec<u8>) -> String {
    let private_key = RsaPrivateKey::from_pkcs1_pem(private_key_pem).unwrap();
    let decrypted_data = private_key.decrypt(Pkcs1v15Encrypt, &encrypted_data).unwrap();
    String::from_utf8(decrypted_data).unwrap()
}

// Swoosh NIKE key generation and exchange
#[pyfunction]
fn swoosh_generate_keys(parameters: (usize, usize, usize)) -> PyResult<(Vec<i8>, Vec<i8>)> {
    let (q, _d, n) = parameters;
    let mut rng = rand::thread_rng();
    let a: Vec<i8> = (0..n * n).map(|_| rng.gen_range(0..q) as i8).collect();
    let s: Vec<i8> = (0..n).map(|_| rng.gen_range(0..q) as i8).collect();
    let e: Vec<i8> = (0..n).map(|_| rng.gen_range(0..q) as i8).collect();
    let public_key: Vec<i8> = a.chunks(n).zip(&s).map(|(row, &s)| (row.iter().sum::<i8>() + e[s as usize % e.len()]) % q as i8).collect();
    Ok((s, public_key))
}

#[pyfunction]
fn swoosh_derive_shared_key(private_key: Vec<i8>, public_key: Vec<i8>, q: usize) -> PyResult<Vec<i8>> {
    let shared_key: Vec<i8> = private_key.iter().zip(&public_key).map(|(&s, &p)| ((s as i16 * p as i16) % q as i16) as i8).collect();
    Ok(shared_key)
}


// Function to convert KyberLibError to PyErr
fn kyber_err_to_pyerr(err: KyberLibError) -> PyErr {
    PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string())
}

// Kyber Functions
#[pyfunction]
fn kyber_keygen(py: Python) -> PyResult<(Py<PyBytes>, Py<PyBytes>)> {
    let mut rng = OsRng;
    let keys = keypair(&mut rng).map_err(kyber_err_to_pyerr)?;
    let public_key = PyBytes::new_bound(py, &keys.public).into();
    let secret_key = PyBytes::new_bound(py, &keys.secret).into();
    Ok((public_key, secret_key))
}

#[pyfunction]
fn kyber_encapsulate(py: Python, public_key: &[u8]) -> PyResult<(Py<PyBytes>, Py<PyBytes>)> {
    let mut rng = OsRng;
    let (ciphertext, shared_secret) = encapsulate(public_key, &mut rng).map_err(kyber_err_to_pyerr)?;
    let ciphertext_bytes = PyBytes::new_bound(py, &ciphertext).into();
    let shared_secret_bytes = PyBytes::new_bound(py, &shared_secret).into();
    Ok((ciphertext_bytes, shared_secret_bytes))
}

#[pyfunction]
fn kyber_decapsulate(py: Python, ciphertext: &[u8], secret_key: &[u8]) -> PyResult<Py<PyBytes>> {
    let shared_secret = decapsulate(ciphertext, secret_key).map_err(kyber_err_to_pyerr)?;
    Ok(PyBytes::new_bound(py, &shared_secret).into())
}

// Module definition
#[pymodule]
fn shadow_crypt(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_dh_key, m)?)?;
    m.add_function(wrap_pyfunction!(derive_dh_shared_key, m)?)?;
    m.add_function(wrap_pyfunction!(generate_ecdh_key, m)?)?;
    m.add_function(wrap_pyfunction!(derive_ecdh_shared_key, m)?)?;
    m.add_function(wrap_pyfunction!(generate_rsa_key, m)?)?;
    m.add_function(wrap_pyfunction!(rsa_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(rsa_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(swoosh_generate_keys, m)?)?;
    m.add_function(wrap_pyfunction!(swoosh_derive_shared_key, m)?)?;
    m.add_function(wrap_pyfunction!(kyber_keygen, m)?)?;
    m.add_function(wrap_pyfunction!(kyber_encapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(kyber_decapsulate, m)?)?;
    Ok(())
}