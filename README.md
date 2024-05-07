# Versión v0.1  agarcisr-TFG

Este es el repositorio para la realización de mi trabajo de fin de grado centrado en el estudio e implementación de protocolos de intercambio de clave no interactivos (NIKE).

## Descripción
Se busca crear un servicio que permita ver, aprender y comparar en base al rendimiento, diferentes tipos de protocolos criptográficos que han sentado las bases e incluso son usados en la actualidad para asegurar la integridad de las comunicaciones, servidores y datos. Para esto, gracias a un desarrollo incremental que sigue las bases de desarrollo ágil, se crearan una serie de iteraciones que vayan sumándole a los pilares establecidos en esta primera versión nuevas funcionalidades y capacidades para culminar en un trabajo de fin de grado que cumpla con todos los objetivos de este estudio de los NIKEs.
En esta primera iteración, se establecen las bases para la implementación de dos protocolos de intercambio de claves, acompañados de una base de datos relacional para la persistencia de diversos componentes y valores que serán visualizados en el frontend.
Por lo tanto se ofrece una demostración práctica de dos protocolos de intercambio de claves fundamentales: Diffie-Hellman y RSA. La implementación se ha llevado a cabo utilizando Python con Flask para el desarrollo de los servicios backend, mientras que para el frontend interactivo se ha empleado Streamlit.

## Componentes

### Base de Datos PostgreSQL

Se utiliza una base de datos PostgreSQL para la persistencia de diversos componentes y valores relacionados con la comunicación y los resultados de los protocolos criptográficos.

#### Tablas Principales

1. **protocols**: Esta tabla almacena la información sobre los protocolos de intercambio de claves, incluyendo su nombre, descripción y endpoint asociado.
2. **protocol_performance**: En esta tabla se registran los resultados de las pruebas de rendimiento de los protocolos, como el tiempo de ejecución de cada prueba y la fecha de registro.

#### Esquema de la Base de Datos

El esquema de la base de datos está diseñado de manera que permita una fácil expansión y mantenimiento. Se siguen las mejores prácticas de diseño relacional para garantizar la integridad y consistencia de los datos almacenados:

![Captura de pantalla 2024-05-07 221447](https://github.com/community/community/assets/63263060/59576c04-df02-496a-bbe7-36efbe947748)
<p align="right"><i>Figura 1</i></p>

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
- **Visualización de Resultados y Comparativa**: Los resultados del proceso de cifrado y las claves utilizadas son mostrados en la interfaz de Streamlit, para lo cual se dispone de la pantalla de comparación de protocolos donde podemos observar las diferentes iteraciones y resultados de los protocolos.

## Navegación y uso

Para utilizar este proyecto, para esta versión sería necesario tener Python y los paquetes requeridos instalados (Flask y Streamlit). Después de clonar el repositorio, se pueden iniciar los servidores Flask con los comandos:


```bash
python app.py
python protocols.py

#El frontend Streamlit se puede iniciar con:
streamlit run streamlit_app.py
```
Una vez que los servidores Flask estén en funcionamiento y el frontend de Streamlit esté ejecutándose, puedes acceder a la aplicación desde tu navegador web por el link proporcionado por consola o accediendo a localhost en el navegador.
La interfaz de usuario es sencilla para su fácil navegación, contando únicamente con dos pestañas en las que alterar y una sidebar visible en todo momento para seleccionar y obtener información de los protocolos.
En la primera pestaña podemos correr el protocolo que se haya seleccionado en nuestra barra lateral. Si la ejecución es exitosa se mostrará un mensaje con el valor del tiempo requerido y otros factores de utilidad para el usuario que se ampliarán en las siguientes iteraciones.
En la segunda pestaña podemos seleccionar diferentes protocolos para ver su comparación y diferencias en cuanto a rendimiento. También se ampliará con más funcionalidades y datos.


## Contribuciones
Este proyecto es parte de mi trabajo de fin de grado. Las contribuciones, sugerencias o preguntas son bienvenidas a través de issues o pull requests en este repositorio.

## Licencia
Este proyecto está bajo una licencia MIT.
