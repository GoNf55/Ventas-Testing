# Ventas-Testing
Proyecto de Gestión de Ventas - Testing UTN 
Proyecto de gestión de ventas simple creado con la finalidad de ser usado en cátedra de Testing - UTN FRVM 
Abarca gestión de ventas, stock y clientes.

## Ejecutar el proyecto localmente
Estos son los paso para ejecutar el proyecto de manera local:
### 1. Clonar el repositorio
Clonar el repositorio con el método de preferencia.
###  2. Creación del entorno virtual
Crear un entorno virtual donde se van a instalar todas las dependencias del proyecto.
```bash
python -m venv venv
```
Activar el entorno virtual para instalar las dependencias
```bash
venv\Scritps\activate
```
Ejecutamos el siguiente comando para realizar la instalación
```bash
pip install -r requirements.txt
```
### 4. Base de datos
El motor de base de datos que utiliza el proyecto es PostgreSql
Debemos crear la base de datos y un usuario. Para eso ingresamos a psql.
```bash
CREATE USER nombre_usuario WITH PASSWORD 'contraseña';
```
```bash
CREATE DATABASE nombre_base_de_datos OWNER nombre_usuario;
```
```bash
GRANT ALL PRIVILEGES ON DATABASE nombre_base_de_datos TO nombre_usuario;
```
### 3. Variables de entorno
Dentro de la carpeta raíz del proyecto creamos un archivo llamado .env , el cual contendrá las variables de entorno que se utilizan.
Reemplazamos los valores de las variables con los datos correspondientes a la BD creada y el usuario creado. Solicitar Secret Key.

``` python
SEC_KEY=''
POSTGRES_DB_NAME='nombre_base_de_datos'
POSTGRES_DB_USER='nombre_usuario'
POSTGRES_DB_PASSWORD='contraseña'
POSTGRES_DB_HOST='localhost'
POSTGRES_DB_PORT='5432' # Cambia el puerto si es necesario
```
### 3. Ejecución del proyecto
Si todo va bien, debemos aplicar las migraciones a la base de datos.
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
Una vez hechas las migraciones, ya podemos ejecutar nuestro proyecto con el siguiente comando
```bash
python manage.py runserver
```
Recordar que django utiliza el puerto 8000 por defecto.