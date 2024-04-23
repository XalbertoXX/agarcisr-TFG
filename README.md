# agarcisr-TFG

Este es el repositorio para la realización de mi trabajo de fin de grado centrado en el estudio e implementación de protocolo de non-interactive key exchange (NIKE).

## Descripción

Este proyecto implementa una demostración práctica de dos protocolos de intercambio de claves: Diffie-Hellman y RSA. Se ha desarrollado utilizando Python con Flask para los servicios backend y Streamlit para el frontend interactivo.

## Componentes

### Backend (Flask)

Se utilizan dos servidores Flask para simular la comunicación entre dos partes utilizando protocolos criptográficos:

1. **app.py** - Servidor que gestiona las solicitudes de intercambio de claves y cifrado de mensajes.
2. **protocols.py** - Servidor que responde a las solicitudes del primer servidor, simula una segunda parte en la comunicación.

#### Funcionalidades:

- **Diffie-Hellman Key Exchange**: Este endpoint en `app.py` inicia un intercambio de claves Diffie-Hellman con el servidor `protocols.py`. Ambos servidores generan claves públicas y privadas, las intercambian y derivan una clave compartida.
- **RSA Encryption and Decryption**: Este endpoint en `app.py` permite enviar un mensaje personalizado que será cifrado usando la clave pública RSA del servidor `protocols.py`. Este servidor luego descifra el mensaje utilizando su clave privada y devuelve el mensaje descifrado para confirmar la validez del proceso.

### Frontend (Streamlit)

La interfaz de usuario está desarrollada utilizando Streamlit, proporcionando una forma visual e interactiva de testear y mostrar los resultados de los protocolos de cifrado:

- **Selección de Protocolo**: Los usuarios pueden seleccionar entre Diffie-Hellman y RSA para probar los protocolos.
- **Entrada de Mensaje Personalizado para RSA**: Cuando se selecciona RSA, los usuarios pueden ingresar un mensaje que será cifrado y luego descifrado por los servidores.
- **Visualización de Resultados**: Los resultados del proceso de cifrado y las claves utilizadas son mostrados en la interfaz de Streamlit.

## Uso

Para utilizar este proyecto, es necesario tener Python y los paquetes requeridos instalados (Flask y Streamlit). Después de clonar el repositorio, se pueden iniciar los servidores Flask con los comandos:


```bash
python app.py
python protocols.py
python streamlit_app.py

#El frontend Streamlit se puede iniciar con:
streamlit run streamlit_app.py
```

## Contribuciones
Este proyecto es parte de mi trabajo de fin de grado. Las contribuciones, sugerencias o preguntas son bienvenidas a través de issues o pull requests en este repositorio.

## Licencia
Este proyecto está bajo una licencia MIT.
