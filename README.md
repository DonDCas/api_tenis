# Backend Tenis

## Francisco Javier Rueda Serrano 

**Index**

[TOCM]

[TOC]


# 0. Introucción

Bienvenido a mi proyecto final para el modulo de Programación de Servicios y Procesos (PSP).
Antes de empezar a explicar como trabajar con este backend quiero explicar que la elección de la tematica viene precedida de ejercicios anteriores de otros modulos que al no haber terminado de forma satisfactoria los he querido expandir un poco por gusto personal y de paso aprovechar para hacer un proyecto más grande.

En este Backend se puede trabajar con una base de datos de jugadores de tenis y competiciones y partidos. La idea es que los usuarios puedan crear y modificar partidos o añadir y modificar jugadores siempre y cuando esten registrados en la base de datos ya sea como admin o como usuarios registrados (arbitros).

La base de datos esta alojada en Postgre y la api esta configurada en base a DJango Rest con lo cual si quieres hacer uso de esta api habra que configurarlos previamente

# 1. Requisitos Previos

Pasemos a la configuración previa del host que alojará nuestro backend.

>[!IMPORTANT]
>Todo lo que se explicará a continuación sobre la instalación esta dirigido a Windows. Si buscar utilizar Linux o MAC deberás amoldar las instalaciones a tu sistema operativo.

## 🐍 Python

>[!NOTE]
>La versión utilizada de Python es (3.14.3) si se usa una anterior o posterior podria dar lugar a errores.

Empezaremos accediendo a la pagina web de python para descargarnos Python Manager a traves del siguiente link [Click aquí](https://www.python.org/downloads "Click aquí")
Una vez descargado iniciamos la instalación marcando la casilla de "**Add Python to Path**"

## 🐈‍⬛ Git

Si vas a querer acceder a este backend desde su repositorio vas a necesitar descargar e instalar como minimo Git a traves de este enlace [Click aqui](https://git-scm.com/install/windows)

## 📯Postman

Vamos a necesitar Postman para hacer pruebas una vez nuestro servidor este en funcionamiento.  Podemos descargarlo si [hacemos click aqui(https://www.postman.com/downloads/)]

# Empezando el proyecto

## 🚀 Desargamos el código

Nos situamos en la carpeta en la que queramos dejar el proyecto y abrimos una terminal.
```bash
git clone https://github.com/DonDCas/api_tenis.git
cd api_tenis
```

Una vez situados en la carpeta del proyecto, api_tenis, instalaremos un entorno de trabajo virtual para nuestro proyecto.

```bash
python -m venv venv
```
Esperamos a que se prepare el proyecto e iniciaremos el entorno virtual

```
#(venv)

.\venv\Script\activate
```

Con esto ya estaremos trabajando en nuestro entorno virtual.

## 📓Instalando dependencias

En el proyecto encontraremos un archivo llamado requirements.txt que incluye todas las dependencias usadas.

```bash
#(venv)

pip install -r requirement.txt
```
El contenido del requeriment contiene las siguientes dependencias:

#### Infraestructura y configuración base
- python-dotenv: Permite cargar variables de entorno desde .env
- psycopg / psycopg-binary: Adaptador para conectar Python y PostgreSQL
- tzdata: Proporciona datos de zonas horarias
- asgiref: Dependencia de Django
- sqlparse: Permite a Django leer SQL

#### Framework Principal

La base del proyecto

- Django
- djangorestframework: Kit de herramientas construir APIs con DJango


#### API y Autenticación

- PYJWT: Librería base para  manejar JSON Web Tokens
- djangorestframework_simplejwt: Implementa la autenticación JWT especifica para Django Rest framework
- django-cors-headers: Permite a la api aceptar peticiones desde otros dominios (Necesaria para despliegues)

#### Gestión y Validación de datos

- django-filter: Permite a los usuarios filtrar los datos en la api mediante la URL
- tablib: Formatea datos en CSV y Excel
- django-import-export: Interfaz ara importar y exportar datos desde el panel de admin
- jsonschema: Valida los archivos JSON
- attrs: Ayuda a crear clases de Python

#### Documentación

- drf-spectacular: Genera documentación con Swager
- PyYAML: Permite leer y escribir archivos YAML
- uritemplate: Ayuda a expandir las URLs en la documentación
- pillow: Libreria para el procesamiento de imagenes
- diff-match-patch: Calcula diferencias entre textos

### 🤫 Preparando .env

En el proyecto encontraras un archivo env.example con el siguiente contenido

```
# --- CONFIGURACIÓN GENERAL DE DJANGO ---
# Cambiar a TRUE para desarrollo local, FALSE para producción
DEBUG=True

# Genera una clave segura para tu proyecto
SECRET_KEY=tu_clave_secreta_aqui

# --- SEGURIDAD Y DOMINIOS ---
# Direcciones IP o dominios permitidos (separados por comas)
ALLOWED_HOSTS=localhost,127.0.0.1,TU_IP_O_DOMINIO

# Orígenes de confianza para formularios y seguridad (incluir http/https)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://tu-dominio.duckdns.org

# --- CONFIGURACIÓN DE BASE DE DATOS (POSTGRESQL) ---
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=usuario_db
DB_PASSWORD=password_seguro_db
DB_HOST=127.0.0.1
DB_PORT=5432

# --- ARCHIVOS MULTIMEDIA ---
# Ruta donde se servirán las imágenes (por defecto /media/)
MEDIA_URL=/media/

```

Tendras que adaptarlo a tu base de datos.

### 🗒️ Preparando la base de datos

Si el archivo .env esta bien configurado solo tendremos que hacer 3 comandos para que se enlacen el proyecto y la base de datos


```bash
# (venv)

# Para analizar modelos y detectar cambios
python manage.py makemigrations

# Aplicar instrucciones segun las modificaciones de los modelos
python manage.py migrate

# Arrancamos el servidor
python manage.py runserver
```


Con esto ya tendremos la API funcionando en: ``http://127.0.0.1:8000``

Para parar el servicio pulsa
<kbd>Ctrl+C</kbd>

# Cómo usar la API

Si todo esta correcto y la api esta en funcionamiento podras acceder sin problemas a

``http://127.0.0.1:8000/api/docs/``

y ver todos los endpoinds que tienes a tu disposición.

##### Hacer ``GET``

Podrás realizar **GET** a todos los endpoinds sin tener que realizar un registro previo.

Estan abiertos varios parametros de busqueda 

-- Jugadores
- Mano dominante
-D
-Z
- Pais
- Nombre

-- Partidos
- Competicion
- Estado
-pen (Pendientes)
-gam (En juego)
-fin (Finalizados)
- fase
-1 - Final
-2 - Semi-Final
-3 - Cuartos de Final
-4 - Octavos de Final
-5 - Dieciseisavos de Final
-6 - 2ª Ronda
-7 - 1ª Ronda
-8 - Fase Previa
-0 - Amistoso


##### Registro

Para poder realizar un registro como usuario deberás realizar un post al endpoint

``http://127.0.0.1:8000/api/register/``

Con el siguiente body:

```JSON
{
  "username": "user_example",
  "email": "user@example.com",
  "password": "string"
}
```

Ahora que tienes un usuario registrado tendras acceso al resto de verbos del CRUD

#### Token

Para poder hacer hacer peticiones se necesita un token que se optiene mediante:

``https://127.0.0.1:8000/api/v1/token/``

Junto con el body

```JSON
{
  "username": "Tu usuario",
  "password": "Tu contraseña"
}
```

Reicibiras en respuesta un token de acceso y uno de refresco para trabajar en webs y refrescar tokens sin necesidad de volver a hacer login.

A partir de aqui cuando quieras hacer una petición de cualquier verbo necesitaras añadir a la cabecera la **Authorization** con el valor
**Bearer Tu_Token**.
