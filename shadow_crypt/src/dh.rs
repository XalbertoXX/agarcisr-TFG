use pyo3::prelude::*;
use num_bigint::{BigUint, RandBigInt};
use rand::thread_rng;

const DH_PRIME: &str = "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF";
const DH_GENERATOR: u32 = 2;

// Diffie-Hellman Functions
#[pyfunction]
pub fn generate_dh_key() -> PyResult<(Vec<u8>, Vec<u8>)> {
    let p = BigUint::parse_bytes(DH_PRIME.as_bytes(), 16).unwrap();
    let g = BigUint::from(DH_GENERATOR);

    let mut rng = thread_rng();
    let private_key = rng.gen_biguint_range(&BigUint::from(2u32), &p);
    let public_key = g.modpow(&private_key, &p);

    Ok((private_key.to_bytes_be().to_vec(), public_key.to_bytes_be().to_vec()))
}

#[pyfunction]
pub fn derive_dh_shared_key(private_key: Vec<u8>, other_public_key: Vec<u8>) -> PyResult<Vec<u8>> {
    let p = BigUint::parse_bytes(DH_PRIME.as_bytes(), 16).unwrap();
    let private_key = BigUint::from_bytes_be(&private_key);
    let other_public_key = BigUint::from_bytes_be(&other_public_key);

    let shared_secret = other_public_key.modpow(&private_key, &p);
    Ok(shared_secret.to_bytes_be().to_vec())
}