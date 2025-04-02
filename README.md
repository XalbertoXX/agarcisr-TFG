# Non Interactive Key Exchange (NIKEs)

Este es el repositorio oficial en el que se ha desarrollado el trabajo de fin de grado de Alberto García Sroda basado en el estudio e implementación de Protocolos de Intercambio de Clave no Interactiva o *NIKEs*.

## Descripcion
Se busca crear un servicio que permita ver, aprender y comparar en base al rendimiento, diferentes tipos de protocolos criptográficos que han sentado las bases e incluso son usados en la actualidad para asegurar la integridad de las comunicaciones, servidores y datos. Para esto, gracias a un desarrollo incremental que sigue las bases de desarrollo ágil, se crearan una serie de iteraciones que vayan sumándole a los pilares establecidos en esta primera versión nuevas funcionalidades y capacidades para culminar en un trabajo de fin de grado que cumpla con todos los objetivos de este estudio de los NIKEs.
En esta primera iteración, se establecen las bases para la implementación de dos protocolos de intercambio de claves, acompañados de una base de datos relacional para la persistencia de diversos componentes y valores que serán visualizados en el frontend.
Por lo tanto se ofrece una demostración práctica de varios protocolos de intercambio de claves que cubren un amplio espectro del cifrado en cuanto a comunicaciones y servicios se refiere a día de hoy como son:

- Diffie-Hellman 
- RSA (*Rivest, Shamir y Adleman*)
- ECDH (*Elliptic-curve Diffie–Hellman*)
- NTRU (*N-th degree Truncated polynomial Ring Units*)
- Crystals Kyber

La implementación se ha llevado a cabo utilizando diferentes lenguajes de programación y recursos que se mencionarán más adelante, cabe destacar de entre todas estas herramientas, el uso del lenguaje de programación Python junto con Rust y las herramientas de contenerización que Docker provee.

---

## Componentes

### Frontend: Streamlit 👑

La interfaz de usuario está desarrollada utilizando Streamlit, esta biblioteca nos permite crear aplicaciones web con una gran calidad visual que cumple con los requisitos más modernos en cuanto a *UX* (user experience) para poder centrar los esfuerzos del deasrollo en crear herramientas útiles y complejas. Esto ha permitido crear esta página con el fin de 

#### 1. **Sidebar**

- **Selección de Protocolo**: Los usuarios pueden seleccionar entre diferentes protocolos criptográficos, bien sea Diffie-Hellman, RSA, NTRU, Crystals Kyber y Elliptic Curve Diffie-Hellman. En este apartado además veremos una información desplegada que nos concretará (dando una referencia más completa a aquellas personas que no tengan un contexto de protocolos muy técnico) datos sobre estos protocolos.
- **Asistente de IA**: Se ha incluido un chat en tiempo real con un modelo de lenguaje de generación de contenido proporcionado por una de las empresas punteras en inteligencia artificial como lo es Google. En este caso es un modelo basado en *gemini-1.5-flash* y el cual permite la interacción directa con una fuente que podrá ayudarnos en cualquier duda que podamos tener así como en 

#### 2. **Overview**

- **Visualización de pantalla principal**: Esta primera pantalla sirve de nexo entre todas las demás, permitiendo ver un resumen de las funcionalidades de la aplicación seguida de unas imágenes de referencia y explicación de los protocolos. Sencilla, minimalista e introductoria, cumple todas las funciones de una página principal.

#### 3. **Test Protocols**

- **Prueba de ejecución de Protocolo**: En este apartado se nos muestra un botón donde podremos lanzar cualquiera de los protocolos que seleccionemos en la barra de navegación izquierda, esto generará una serie de respuestas que en caso de ir correctamente, nos mostrarán lo que se explica más adelante.
- **Visualización de Resultados Inmediatos**: Los resultados del proceso de cifrado y las claves utilizadas son mostrados en esta página junto con un resumen de los datos que se almacenan de estos procesos matemáticos así como una explicación de todo lo ocurrido durante la ejecución de las pruebas. Estos datos incluyen tiempo de respuesta, consumo de banda durante el intercambio del protocolo y, como añadido, la longitud de la información extra añadida, útil para ver cuánto puede desviar esto al protocolo RSA en cuanto a cifrado se refiere debido a que es el único que permite un input para cifrar. Sirve de nexo a la tercera pantalla donde podremos observar cómo se acumulan estos datos en las diferentes gráficas que tenemos disponibles para el usuario en la tercera pestaña.

#### 4. *Compare Protocols*

- **Elemento de selección de resultados**: Para esta última pestaña tenemos una barra de selección donde podremos elegir los protocolos que formarán parte de la muestra de esta comparativa.
- **Gráfica de tiempo de respuesta**: Tras elegir los protoclos se nos muestra una gráfica dinámica y totalmente interactuable para poder elegir la escala y fragmento que queramos comparar entre los diferetnes protocolos.
- **Gráfica de consumo de banda ancha**: Se proporciona una gráfica donde se puede observar el consumo medio para la realización de cada protocolo de banda ancha. Útil para la comparativa en diferentes aspectos referentes a la eficiencia de cada uno de los protoolos.
- **Gráfica de adición de recursos externos**: Permite ver los megabytes de información añadida para protocolos donde se busque el cifrado al uso de información como sería RSA.
- **Comparativas directas**: Más adelante se observan diferentes tablas que comparan directamente valores como media y mediana de cada elemento para determinar cual es el mejor en correspondencia a todos estos valores proporcionados.

Estas son las funcionalidades de la página sumados a una explicación detallada de cada servicio que ofrece. A continuación se detallarán los elementos que subyacen a todos etos apartados para permitir el correcto funcionamiento del aplicativo.

### Base de Datos: 📊 PostgreSQL & Supabase ⚡

Se utiliza una base de datos PostgreSQL para la persistencia de diversos componentes y valores relacionados con la comunicación y los resultados de los protocolos criptográficos así como el almacenamiento de diferentes compoenentes de texto. Esta base de datos corre en los servicios de Supabase, la cual es una empresa de hosting que permite tener una base de datos corriendo en sus servidores, asegurándonos la continua accesibilidad a los datos por parte de cualquier usuario.

#### Tablas Principales

1. **protocols**: Esta tabla almacena la información sobre los protocolos de intercambio de claves, incluyendo su nombre, descripción breve, más detallada y extensa de este, endpoint asociado para ser llamado en los servicios.
2. **protocol_performance**: En esta tabla se registran los resultados de las pruebas de rendimiento de los protocolos, como el tiempo de ejecución de cada prueba y la fecha de registro.
3. **protocol_visuals**: En esta tabla se incluyen elementos visuales como imágenes para permitir su visualización en la web mediante un almacenaje eficiente.
4. **webpage_contents**: En esta tabla se registra el texto de la página principal, quitando carga visual al código y haciendo un uso más profesional de los recursos.
#### Esquema de la Base de Datos

El esquema de la base de datos está diseñado de manera que permita una fácil expansión y mantenimiento, siguiendo las mejores prácticas de diseño relacional para garantizar la integridad y consistencia de los datos almacenados:

![image](https://github.com/user-attachments/assets/b068a589-eb8b-4c84-9ed0-3115439df032)
<p align="right"><i>Figura 1</i></p>

### Backend: ⚗️ Flask & Docker 🐳

Se utilizan dos servidores Flask para simular la comunicación entre dos partes involucradas en la comunicación ya sea para el cifrado, aseguramiento de sesión segura, canal, etc. Para cada servidor creamos un contenedor que nos permite empaquetar el aplicativo en dos unidades encapsuladas, facilitando la subida de estos servicios a plataformas de despliegue en la nube. 
Estos elementos se encuentran recogidos en el directorio *service*, donde podremos encontrar en *server1* y *server2* los componentes mencionados previamente. Por ello tendremos los ficheros *Dockerfile* necesarios para levantar los contenedores donde correrán ambos servicios.

1. **f_server_1.py** - Actúa como servidor A que gestiona las solicitudes de intercambio de claves y cifrado de mensajes, inicia la comunicación tras ser llamado por el aplicativo a través de una consulta del usuario. Este se encarga posteriormente de reunir en un formato .json toda la información recogida de la respuesta del servidor B
2. **f_server_2.py** - Servidor que responde a las solicitudes del primer servidor, simula una segunda parte en la comunicación, en este caso encargándose de descifrar o generar componente necesaria para establecer la veracidad de su instacia.


### Librerías implementadas: 🦀 Rust 

Debido a requerimientos funcionales y decisiones de diseño se decidió crear una librería en un lenguaje que pudiera ir a más bajo nivel que Python, como lo es Rust, para poder llevar al máximo exponente elementos como la confidencialidad, seguridad y robsutez de los datos manejados por los protocolos. 
Huyendo así de ciertas restricciones que nos causaba Python a la vez que se nos permitía aumentar la velocidad de cómputo al eliminar la interpretación de Python. Esto supuso una gran ventaja ya que se lidia con claves de gran tamaño (2048 bit resistentes). Por ello, y sirviéndonos de librerías como *Pyo3* juntada con la extensión *maturin*, pudimos generar una librería propia de código abierto realizada puramente en el lenguaje de programación , la cual es visible y completamente accesible desde [*PyPI*](https://pypi.org/project/shadowcrypt/).

![image](https://github.com/user-attachments/assets/0b98f784-63ef-40ee-ad37-dbcd243a1ef4)
<p align="right"><i>Figura 2</i></p>

La librería es posteriormente usada por los ya mencionados servidores para poder emplear las diferentes operaciones criptográficas de una forma eficiente.

- Estructura

![image](https://github.com/user-attachments/assets/521fec78-ec0b-4304-b1bb-5f2cfda96d57)
<p align="right"><i>Figura 2</i></p>

Para llevar a cabo esta librería recurrimos a la modularización y el uso de patrones de diseño para asegurar que cada apartado era conciso y competente para su función, especificando que cada elemento cumpliera con la solución al problema de no poder desarrollar estos protocolos en Python por lo ya comentado previamente. Esto hizo que se divieran en 5 ficheros .rs para cada protocolo con un lib.rs que gestiona todas las funciones que cada fichero provee para que sean usados en Python por los servicios posteriormente.

---

## Navegación y uso 🌐

Para utilizar este proyecto basta con acceder a la página web oficial totalmente funcional!

- **https://agarcisr-tfg-q3snv9fb7ct3lpknrpeakpnikesh.streamlit.app/** 

Esta es accesible completamenta al estar desplegada en un entorno cloud gracias a los servicios de [*Streamlit cloud*](https://streamlit.io/cloud) así como los servidores de hosting de la plataforma [*Render*](https://render.com/).
 
## Contribuciones
Este proyecto es parte de mi trabajo de fin de grado. Las contribuciones, sugerencias o preguntas son bienvenidas a través de issues o pull requests en este repositorio.

## Licencia
Este proyecto está bajo una licencia [MIT](http://www.apache.org/licenses/LICENSE-2.0) otorgada por apache.

> _NIKEtfg_
