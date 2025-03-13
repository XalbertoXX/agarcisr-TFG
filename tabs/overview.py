import streamlit as st

# Main page
def show_overview():
    st.title("Welcome to the Protocol Performance Testing App! 🚀")
    st.markdown("""
    ### Purpose
    This app allows users to test and compare the performance of various cryptographic protocols.  
    Cryptographic protocols are crucial for secure communication, especially in the age of quantum computing and cyber threats.
    These reasons are what inspire the creation of this website, as it is important to understand the performance characteristics 
    of these protocols to make informed decisions when implementing secure systems.

    ### Usage
    Here we will be testing some of the most popular protocols, and some of the most secure ones, to see how they perform in real time.
    - **Search for a Protocol**: Use the search bar on the right to quickly find protocols of interest by name or description.
    - **Test Protocols**: You can get in depth explanations of the protocols and test them by clicking the button below, where 
    you can also see the response time of the server alongside some other metrics.
    - **Compare Protocols**: Thanks to the usage of different visualizations, you can compare the performance of different protocols 
    in real time, and see which one is the best in terms of performance while also seeing the average response time and the standard deviation of each protocol.

    ### History of Protocols
    Cryptographic protocols have evolved significantly over time. At its core, protocols are sets of rules that govern the secure exchange of information.
    This allowerd the creation of secure communication channels, and the ability to encrypt and decrypt messages, ensuring the privacy and integrity of the data,
    evolving into the protocols we know today. These are able to secure not just the data, but also the communication channels, and the identities of the parties involved,
    ensuring the sessions that run daily communications, transactions, and more.
    
    To get a wider scope of the different resources we wanted to provide, here is a brief history of some of the most popular protocols:
    - **Good old days**: Diffie-Hellman and RSA were some of the first protocols to be developed, and are still widely used today, although they differ in the way they encrypt and decrypt messages
    and in the way they are used. While Diffie-Hellman is used to establish secure communication channels through key exchange by using prime numbers to generate the keys, RSA is used to encrypt and decrypt messages
    using the public and private keys of the parties involved. They were pioneers in the field of cryptography, and are still used today, although they are not as secure as they used to be. This gets us to the next point.
                
    - **Evolving to the future**: Elliptic Curve Cryptography (ECC) is a more modern protocol that is used to secure communication channels and encrypt messages, it is based on the mathematical properties of elliptic curves          
    and we have the perfect example to showcase this, the Elliptic Curve Diffie-Hellman (ECDH) protocol, which is used to establish secure communication channels through key exchange, and is considered to be more secure 
    than the traditional Diffie-Hellman protocol. This is because it uses smaller key sizes to achieve the same level of security, which makes it more efficient and faster while aiming for quantum resistance.
                
    - **Quantum Computing**: The advent of quantum computing has posed new challenges to traditional cryptographic systems. Quantum computers leverage quantum bits (qubits) to perform computations,
    which can solve certain problems much faster than classical computers can, setting a new paradigm in the way we understand security.
    This is why it is important to test and compare the performance of these protocols, as they are the ones that will be used in the future to secure the data and the communication channels
    and can showcase the viability of the current solutions we have in place.
    - Quantum computers can break widely-used protocols like RSA and Diffie-Hellman, due to their ability to factor large numbers efficiently.
    In order to fight this, alongside the usage of elliptic curve cryptography, there are other proposals such as lattice-based cryptography and learning with errors (LWE), and we chose two contenders to fend off the quantum threat:
    - **Cristal Kyber**: A lattice-based cryptography protocol that uses the hardness of the learning with errors (LWE) which revolves around the hardness of finding the error in a noisy system of equations to secure the data and the communication channels.
    - **NTRU**: A lattice-based cryptography protocol that uses the hardness of the shortest vector problem (SVP) to secure the data and the communication channels. This one differs from the previous one as it uses the 
    hardness of finding the shortest vector in a lattice to secure the data and the communication channels.
                

    ### Why This App?
    This application is designed to provide an intuitive way to test, compare and learn what are otherwise considered to be "opace" and complex algorithms that secure everyday technology.
    Mixing usability and complexity isn´t easy, but trying to get close to the user and having graphs and real time data can help to understand them a bit better 🤓!
    """)