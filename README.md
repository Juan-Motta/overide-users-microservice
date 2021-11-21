# OVERIDE - Microservicio de autenticación y manejo de usuarios

<p align="center">
  <img src="https://user-images.githubusercontent.com/78517969/142134016-fb38944a-ca4a-4c40-9c4f-c9ff762bc9b0.png" alt="DB_Model" />
</p>


Microservicio de manejo de usuarios y autenticación de la applicacion OVERIDE, contiene toda la logica para el manejo de usuarios y autenticación mediante el uso de una API Rest junto con JWT.

![arquitectura users drawio (1)](https://user-images.githubusercontent.com/78517969/141705455-130dc501-b087-4753-a1dd-e045b46a4b40.png)

## 💻 Requisitos

* Python 3.9
* PostgreSQL
* Docker

## 🛠️ Guia de configuracion

El proyecto se encuentra corriendo bajo un host de docker, es posible utilizar el proyecto de manera local utilizando python o utilizando docker

<hr>

### Creacion de variables de entorno
En la raiz del proyecto se debe crear un archivo con el nombre **.env** con la siguiente informacion

```
DEBUG=<Boolean: False o True>
DB_NAME=<nombre db>
DB_USER=<usuario de la db>
DB_PASSWORD=<contraseña de la db>
DB_HOST=<host de la db>
DB_PORT=<puerto de la db>
SECRET_KEY=<secret key, puede ser cualquier string>
```

La informacion suministrada no debe tener comillas o espacios

### Configuración tradicional

La guia de configuracion esta creada bajo comandos de Windows. Todos los comandos se deben realizar en la raiz del proyecto (carpeta del proyecto) a la altura del archivo manage.py.

#### 1️⃣ Crear entorno virtual
```console
python -m venv venv
```

#### 2️⃣ Ejecutar entorno virtual
```console
.\venv\Scripts\activate
```

#### 3️⃣ Instalar dependencas del proyecto
```console
pip install -r requirements.txt
```

#### 4️⃣ Realizar migraciones
```console
python manage.py makemigrations
```
```console
python manage.py migrate
```

#### 5️⃣ Crear superusuario
```console
python manage.py createsuperuser
```

#### 6️⃣ Inicio del servidor
```console
python manage.py runserver
```
<hr>

### Configuracion via Docker

La guia de configuracion esta creada bajo comandos de Windows. Todos los comandos se deben realizar en la raiz del proyecto (carpeta del proyecto) a la altura del archivo manage.py.

#### 1️⃣ Inicio del servidor Docker
```console
docker-compose up
```

#### 3️⃣ Crear superusuario
De ser necesario es posible crear un superusuario con el comando
```console
docker-compose exec users python3 manage.py createsuperuser
```

Para cerrar el servidor una vez inicializado se debe usar el comando:

#### ⏹️ Cerrar servidor Docker
```console
docker-compose down -v
```
<hr>

## ⚙️ API

Un usuario solo podra obtener, modificar y eliminar su propia información, solo los usuarios con permisos de administrador pueden acceder y modificar la información de otros usuarios.

#### 🟢 Obtener usuario
Devuelve el usuario que corresponda al id especificado, si no existe devuelve un mensaje de error
```
http://localhost:8000/api/users/<int:id>
```

Ejemplo: 

```
http://localhost:8000/api/users/1
```
```json
{
    "id": 1,
    "username": "jhon",
    "email": "jhon@example.com",
    "name": "Jhon",
    "last_name": "Doe",
    "document": "12345678",
    "birth": "2021-11-15",
    "phone": "12345678",
    "is_active": true,
    "is_staff": false
}
```


#### 🟢 Obtener usuarios
Devuelve una lista con todos los usuarios registrados
```
http://localhost:8000/api/users
```

#### 🟢 Crear usuario
Crea un usuario con la información suministrada. Id, is_active e is_staff no deben ser suministrados o no se tendran en cuenta.
```
http://localhost:8000/api/users/
```

Ejemplo:

```
http://localhost:8000/api/users/
```
```json
{
    "username": "jhon",
    "email": "jhon@example.com",
    "name": "Jhon",
    "last_name": "Doe",
    "document": "12345678",
    "birth": "2021-11-15",
    "phone": "12345678",
}
```

#### 🟢 Editar usuario
Modifica el usuario que corresponda al id suministrado, la información que se debe suministrar corresponde a la misma que la de crear un usuario.
```
http://localhost:8000/api/users/<int:id>
```

#### 🟢 Eliminar usuario
Elimina el usuario que corresponda con el id suministrado
```
http://localhost:8000/api/users/<int:id>
```

#### 🟢 Obtener token
Devuelve un par de tokens de acceso si las credenciales de acceso existen en la base de datos. **La duración del access token es de 5 minutos**
```
http://localhost:8000/api/token/
```

Ejemplo:
```
http://localhost:8000/api/token/
```
```json
{
    "username": "jhon",
    "password": "contraseña123"
}
```

#### 🟢 Refrescar token
Devuelve acces token nuevo si el refresh token suministrado es valido. **La duración del refresh token es de 1 dia**
```
http://localhost:8000/api/token/refresh/
```

Ejemplo:
```
http://localhost:8000/api/token/refresh/
```
```json
{
    "refresh": "asdadasd7ad7afad67a5a28asda8da8das8da...",
}
```

## 📝 Notas

#### 0.1.0

* Inicio del proyecto
* Creada configuracion inicial del proyecto
* Agregadas dependencias del proyecto
* Creadas variables de entorno
* Agregada app users

#### 0.2.0

* Creados servicios REST asociados a la app users
* Agregado servicio de autenticacion por medio de JWT

#### 0.3.0

* Actualizada seguridad de la API, ahora solo es posible acceder a la informacion del usuario con el id entregado el las cabeceras de la aplicación.
* Actualizada seguridad de la API, ahora los usuarios con permisos de administrador pueden acceder a la informacion de cualquier usuario.
