# COLORS 🎨✨🔍

COLORS es una aplicación diseñada para **escrapear colores y paletas** de sitios web. Permite a los usuarios seleccionar un color (previamente obtenido mediante scraping) y conectarlo con la base de datos para encontrar combinaciones y generar distintas paletas de colores.

## Estado del MVP 🚀🎯📊

En la primera versión del MVP, solo se han recopilado los colores mediante scraping. En futuras mejoras, se optimizará la relación entre las bases de datos para mejorar la experiencia del usuario y generar combinaciones de colores de manera más fluida y eficiente.

## Instalación y Ejecución 🖥️⚙️📂

### 1. Clonar el repositorio

```sh
git clone https://github.com/tu_usuario/colors.git
cd colors
```

### 2. Crear y activar un entorno virtual (Opcional pero recomendado)

#### En Windows:

```sh
python -m venv venv
venv\Scripts\activate
```

#### En macOS/Linux:

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```sh
pip install -r requirements.txt
```

### 4. Aplicar migraciones y configurar la base de datos

```sh
python manage.py makemigrations #Crear base de datos en sql 
python manage.py migrate
```

### 5. Ejecutar el servidor de desarrollo

```sh
python P3_Web_Scraping_Steph/manage.py scrape
```


## Mejoras futuras 🚧📈🔄

- Implementar la relación de colores en la base de datos para generar paletas automáticamente.
- Optimizar el sistema de scraping para obtener combinaciones de colores desde múltiples fuentes.
- Mejorar la interfaz de usuario para hacer la selección y visualización de paletas más intuitiva.

## Tecnologías utilizadas 🛠️📌💡

Control de versiones: Git / GitHub
Lenguaje principal: Python
Librerías útiles: Selenium
Bases de datos: SQL
Gestión del proyecto: Github
Para manejar las imágenes de los colores: Pillow 

### 📊 Se consideraron los siguientes criterios

✅ Gestión eficiente del proyecto con herramientas de control de versiones.
✅ Desarrollo de un programa funcional en Python.
✅ Diseño y gestión efectiva de bases de datos.
🟢 Nivel Esencial:
✅ Script que accede a un sitio web y extrae información.
✅ Limpieza y organización de datos.
✅ Documentación del código y un README en GitHub.
🟡 Nivel Medio:
✅ Almacenamiento de los datos en una base de datos.


## Contribución 🤝🎨🚀

Si deseas contribuir al proyecto, siéntete libre de abrir un issue o hacer un pull request. ¡Toda ayuda es bienvenida! 🎨🚀

