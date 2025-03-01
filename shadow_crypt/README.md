# Shadow Crypt

Shadow Crypt is a Rust-based cryptographic library built with [PyO3](https://pyo3.rs/) and [maturin](https://maturin.rs/). It provides Python bindings for a suite of cryptographic protocols including:

- **Kyber** (Post-Quantum Cryptography using Kyber512)
- **NTRU** (Lattice-based cryptography with parameters equivalent to NTRU-HPS-2048)
- **ECDH** (Elliptic Curve Diffie–Hellman using X25519)
- **Diffie–Hellman (DH)** (Classical DH using a 2048-bit safe prime)
- **RSA** (2048-bit RSA for encryption/decryption)

The library is designed to offer comparable security levels (~128-bit security) across different protocols, making it ideal for benchmarking encryption/decryption times and analyzing bandwidth usage.

## Features

- **Multi-Protocol Support:** Compare and benchmark classical and post-quantum cryptographic protocols in a unified framework.
- **Python Integration:** Use the library seamlessly in Python projects (e.g., Flask servers) through PyO3.
- **High Performance:** Leverage Rust’s performance and safety for cryptographic operations.
- **Extensibility:** Easily add new cryptographic primitives or adjust parameters for detailed performance analysis.

## Installation

### Prerequisites

- Rust (with Cargo)
- Python 3.7+
- [Maturin](https://maturin.rs/) (install via pip)

```bash
pip install maturin