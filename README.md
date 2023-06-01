
# Fast API DB

Este es un repositorio contiene el desarrollo de una REST API la cual se conecta una base de datos (SQLite) para guardar informacion proporcionada por el usario a partir de archivos en excel (.xlsx). Además, procesa y valida la informacion para generar un archivo .xlsx con todos los datos recolectados.


## Instalación

Para instalar el proyecto se necesita instalar la librería *vitualenv* de Python usando el siguiente comando.

```bash
pip install virtualenv
```

Situarnos en la carpeta del repositorio y crear un nuevo ambiente virtual por medio de:
```bash
cd \path\del\repositorio
python -m venv <nombre-de-ambiente>
```

Activamos el ambiente virtual creado:
```bash
<nombre-de-ambiente>\Scripts\activate
```

Por último, instalamos las dependencias del proyecto en el archivo *requirements.txt*

```bash
pip install -r requirements.txt
```

## Correr Localmente 

Para correr el proyecto, nos conectamos al servidor de uvicorn mediante:

```bash
uvicorn app.main:app --reload
```

Damos click en la URL que nos genera para conectarnos a la API. Para ver la documentación y el monitoreo de la misma, visitamos la ruta:

- (eg.) http://127.0.0.1:8000/docs
## REST API

Esta applicacióm fue creada con ayuda del framework [*FastAPI*](https://fastapi.tiangolo.com/lo/). Cuenta con las siguentes funciones principales:

### *Upload payments*
*URL:* `POST \payments`

Se puede subir los pagos proporcionado un archivo excel (.xlsx) validando la información para posteriormente subirla a la base de datos. 

*Nota:* El archivo debe estar en extensión `.xlsx` de otra manera regresará un código `400` de archivo invalido. También regesara un json especificando el tipo de error en la validación.

#### Respuesta
```javascript
 {"Data" : "'<file_name>' Uploaded Successfully!"}
```

### *Download Excel*
*URL:* `GET \payments`

Regresa mediante un archivo excel todos los registros alojados en la DB.

### *Get Total*
*URL:* `GET \payments-total`

Retorna un json con la suma total de todos los pagos registrados.

#### Respuesta

```javascript
{"Data": "La suma total de los pagos es: <total>"}
```




## Validación

Dentro de algoritmo de validación, existen una serie de condiciones para que el programa de el visto bueno para proceder a subir a la bases de datos:

- **NO sea nulo:** Se considera que todas las columnas tengan un valor ya que todas ellas son relevantes para registrar.

- **Tipo de dato sea correcto:** Es decir, no se pueden registrar *montos* que sean palabras, ni *fechas* que sean numeros decimales.

Gracias a la librería [*Pandas*](https://pandas.pydata.org/) se leen los archivos de Excel (.xlsx) y los convierte a un dataframe el cual facilita la manipulación de los datos en python y así leer y checar los puntos previamente mencionados de posibles inconsistencias en los datos.
## Base de Datos

Para el diseño de la base de datos se considero que eran necesarias 3 tablas: una para los clientes, proveedores, y pagos. Ya que, se puede agregar información que sea relevante para los clientes o proveedores (eg. correo, edad, etc). Elimiando información irrelevante o redundante entre tablas sobre todo el registro de los pagos. A continuación, se muestra la estuctura de las tablas en la DB.

#### Clientes

| id (primary key) | nombre |
| :-------- | :------- | 
| `int` | `string` |

#### Proveedores

| id (primary key) | nombre |
| :-------- | :------- | 
| `int` | `string` |

#### Pagos

| id (primary key) | fecha | cliente_id (foreign key) | monto | proveedor_id (foreign key) |
| :--------------- | :---- | :--------- | :---- | :---------- |
| `int` | `datatime` | `int` | `float` | `int` |


Se hizo uso de la librería [*SQLAlchemy*](https://www.sqlalchemy.org/) para dar la funcionalidad a la API de conectarse a una base de datos y obtener y subir información.

Dentro del la carpeta `app` se encuentran los siguentes archivos necesarios para conectarse a la DB:
- `database.py` : se encuentra todo lo necesario para iniciar sesión a una Base de Datos.
- `models.py` : se diseñan las tablas espeficando: los nombres, el tipo de dato y sus relaciones entre tablas.
- `schemas.py` : ya que se usa un modelo ORM se especifica la estuctura de estos esquemas que convierten los datos recibidos a un objeto en código para facilitar su manejo posteriormente.
- `crud.py` : contiene los querys de la DB que se van a estar usando la applicación, eg. crear pagos, obtener clientes, obtener cliente por id, etc.
## Hallazgos y Recomendaciones

[*FastAPI*](https://fastapi.tiangolo.com/lo/) brinda la posibilidad de subir archivos y descargar un archivo en respuesta importando `UploadFile` y `FileResponse`. Me parecio una buena idea integrar estas 2 funcionalidades, ya que es más practico para el usuario ir subiendo los excel a las DB, y obteniendo excel con todos los datos guardados. Usando `content_type` se puede checar el tipo de archivo para validar a la hora subirlo, asi evitando posibles errores.

Para poder visualizar las tablas de la DB se recomienda instalar [DB Browser for SQLite](https://sqlitebrowser.org/) y abrir `sql_app.db`.