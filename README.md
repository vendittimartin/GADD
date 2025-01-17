## Manual de usuario

Esta aplicación te permite encontrar imágenes similares dentro de un conjunto de datos en base a sus características visuales.

### Instalación

1. **Requisitos previos:**
    - Asegúrate de tener Python 3.8 o superior instalado. Puedes verificarlo ejecutando `python3 --version` en tu terminal.
    - Descarga e instala PostgreSQL desde [https://www.postgresql.org/download/](https://www.postgresql.org/download/).

2. **Instalar dependencias:**
    - Instala Flask y otras bibliotecas necesarias:
        ```bash
        pip install Flask psycopg2 werkzeug numpy torch torchvision Pillow
        ```

3. **Configurar la conexión a la base de datos:**
    - Modifica el archivo `config.json` reemplazando los valores con los valores correspondientes a tu base de datos y ruta del proyecto:

        ```json
        {
            "dbname": "tu_nombre_de_base_de_datos",
            "user": "tu_usuario_de_base_de_datos",
            "password": "tu_contraseña_de_base_de_datos",
            "host": "tu_host_de_base_de_datos",
            "port": "tu_puerto_de_base_de_datos",
            "static_dataset": "ruta/a/tu/conjunto_de_datos/de_imágenes",
            "input_path": "ruta/para/almacenar/imágenes/cargadas"
        }
        ```
        - Las rutas utilizadas se encuentran escritas como rutas relativas. 
        - `static_dataset`: Esta es la ruta al directorio que contiene las imágenes del conjunto de datos inicial que se utilizan para la comparación.
        - `input_path`: Esta es la ruta donde se almacenarán las imágenes cargadas.

4. **Crear el esquema de la base de datos:**
    - Ejecuta el script ubicado en `/scripts/database.sql` en tu base de datos configurada anteriormente.

### Ejecución de la aplicación

1. **Inicia el servidor:**
    - Abre tu terminal y navega hasta el directorio del proyecto.
    - Ejecuta el siguiente comando:
        ```bash
        python app.py
        ```
    - Esto iniciará el servidor Flask, generalmente accesible en `http://localhost:5000/` o `http://127.0.0.1:5000/`.

### Uso de la aplicación

1. **Carga el conjunto de datos:**
    - Accede a `http://localhost:5000/` o `http://127.0.0.1:5000/` en tu navegador web.
    - Haz clic en el botón "Cargar datos". Esto procesará las imágenes de tu directorio de conjunto de datos especificado (`static_dataset` en tu base de datos configurada dentro de `config.json`) y poblará la tabla de la base de datos.
    - La aplicación devolverá un `load_data status 200` cuando se haya finalizado la carga de datos.

2. **Encuentra imágenes similares:**
    - Haz clic en el botón "Seleccionar Imagen" y elige un archivo de imagen (jpg o jpeg).
    - Haz clic en el botón "Consultar".
    - Esto cargará la imagen, extraerá sus características y encontrará imágenes similares en la base de datos.
    - La página de resultados mostrará tu imagen cargada y las imágenes similares del conjunto de datos, junto con sus valores de similitud.

3. **Ver más imágenes similares (opcional):**
    - La página de resultados puede tener un botón "Mostrar más". Al hacer clic en él, se desplegarán más imágenes similares del conjunto de datos.
