use pyo3::prelude::*;
use pyo3::types::PyBytes;
use rand::rngs::OsRng;
use kyberlib::*;

fn kyber_err_to_pyerr(err: KyberLibError) -> PyErr {
    PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string())
}

// Kyber key generator
#[pyfunction]
pub fn kyber_keygen(py: Python) -> PyResult<(Py<PyBytes>, Py<PyBytes>)> {
    let mut rng = OsRng;
    let keys = keypair(&mut rng).map_err(kyber_err_to_pyerr)?;
    let public_key = PyBytes::new_bound(py, &keys.public).into();
    let secret_key = PyBytes::new_bound(py, &keys.secret).into();
    Ok((public_key, secret_key))
}

// Kyber keypair encapsulation
#[pyfunction]
pub fn kyber_encapsulate(py: Python, public_key: &[u8]) -> PyResult<(Py<PyBytes>, Py<PyBytes>)> {
    let mut rng = OsRng;
    let (ciphertext, shared_secret) = encapsulate(public_key, &mut rng).map_err(kyber_err_to_pyerr)?;
    let ciphertext_bytes = PyBytes::new_bound(py, &ciphertext).into();
    let shared_secret_bytes = PyBytes::new_bound(py, &shared_secret).into();
    Ok((ciphertext_bytes, shared_secret_bytes))
}

// Kyber keypair decapsulation
#[pyfunction]
pub fn kyber_decapsulate(py: Python, ciphertext: &[u8], secret_key: &[u8]) -> PyResult<Py<PyBytes>> {
    let shared_secret = decapsulate(ciphertext, secret_key).map_err(kyber_err_to_pyerr)?;
    Ok(PyBytes::new_bound(py, &shared_secret).into())
}