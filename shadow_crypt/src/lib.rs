use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

mod dh;
mod ecdh;
mod rsa;
mod kyber;
mod ntru;
mod sidh;

use dh::{generate_dh_key, derive_dh_shared_key};
use ecdh::{generate_ecdh_key, derive_ecdh_shared_key};
use rsa::{generate_rsa_key, rsa_encrypt, rsa_decrypt};
use kyber::{kyber_keygen, kyber_encapsulate, kyber_decapsulate};
use ntru::{ntru_generate_keypair, ntru_encapsulate, ntru_decapsulate};


#[pymodule]
fn shadow_crypt(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_dh_key, m)?)?;
    m.add_function(wrap_pyfunction!(derive_dh_shared_key, m)?)?;
    m.add_function(wrap_pyfunction!(generate_ecdh_key, m)?)?;
    m.add_function(wrap_pyfunction!(derive_ecdh_shared_key, m)?)?;
    m.add_function(wrap_pyfunction!(generate_rsa_key, m)?)?;
    m.add_function(wrap_pyfunction!(rsa_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(rsa_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(kyber_keygen, m)?)?;
    m.add_function(wrap_pyfunction!(kyber_encapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(kyber_decapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(ntru_generate_keypair, m)?)?;
    m.add_function(wrap_pyfunction!(ntru_encapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(ntru_decapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(sidh::sidh_keygen, m)?)?;
    m.add_function(wrap_pyfunction!(sidh::sidh_encapsulate, m)?)?;
    m.add_function(wrap_pyfunction!(sidh::sidh_decapsulate, m)?)?;
    Ok(())
}