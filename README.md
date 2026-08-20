# Mapa Vivo

Mapa Vivo es una plataforma web para registrar y consultar puntos de apoyo humanitario en Colombia. Los gestores pueden registrar puntos, reportar necesidades y actualizar su estado; los donantes pueden consultar el mapa y el detalle de las necesidades activas.

## Funcionalidades

- Mapa público de puntos de apoyo: albergues, centros de acopio, rescate y logística, edificios colapsados, entre otros.
- Registro de gestores y puntos con ubicación seleccionada en mapa.
- Perfiles de usuario con roles: administrador, gestor y donante.
- Registro de necesidades por categoría y subcategoría.
- Actualización del estado de atención de cada necesidad.
- Administración mediante Django Admin.

## Requisitos

- Python 3.12 o superior.
- Git.
- Acceso a Internet para cargar el mapa base de OpenStreetMap y Leaflet.

> El proyecto usa SQLite para desarrollo local, por lo que no requiere instalar un servidor de base de datos.

## Instalación local

### 1. Clonar el repositorio

```bash
git clone https://github.com/leidy-jaramillo/MapaVivo.git
cd MapaVivo
```

### 2. Crear y activar un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Crear la base de datos

Ejecuta las migraciones para crear las tablas y cargar los catálogos de ciudades, tipos de punto, categorías y subcategorías:

```bash
python manage.py migrate
```

### 5. Crear un administrador

```bash
python manage.py createsuperuser
```

Ingresa el usuario, correo y contraseña solicitados. Este usuario tendrá el rol de administrador automáticamente.

### 6. Iniciar el servidor

```bash
python manage.py runserver
```

Abre estas direcciones en el navegador:

- Aplicación pública: `http://127.0.0.1:8000/`
- Administración: `http://127.0.0.1:8000/admin/`

Para detener el servidor, presiona `Ctrl + C` en la terminal.

## Primer uso

1. Accede a `/admin/` con el superusuario.
2. Revisa o crea gestores desde **Usuarios** y asigna su rol en **Perfiles de usuario**.
3. Los gestores pueden crear puntos de apoyo desde la aplicación y registrar necesidades desde su perfil.
4. Confirma los puntos revisados desde el administrador cambiando su estado de verificación.
5. Los donantes consultan el mapa público y pueden abrir el detalle de necesidades activas.

## Roles

| Rol | Acceso |
| --- | --- |
| Administrador | Admin Django, creación de usuarios, puntos y gestión total. |
| Gestor | Registra y edita sus propios puntos; registra necesidades y actualiza sus estados. |
| Donante | Consulta el mapa público y las necesidades activas. |

## Estructura principal

```text
mapavivo/      Configuración del proyecto Django
perfiles/      Roles y perfiles de usuario
puntos/        Tipos, ciudades y puntos de apoyo
reportes/      Necesidades, categorías y subcategorías
portal/        Vistas, formularios y páginas públicas
static/        Estilos CSS
templates/     Plantillas HTML
```

## Notas para producción

Antes de publicar la aplicación en Internet:

- Cambia `SECRET_KEY` por una variable de entorno privada.
- Configura `DEBUG = False`.
- Define correctamente `ALLOWED_HOSTS`.
- Usa PostgreSQL u otra base de datos administrada en lugar de SQLite.
- Configura almacenamiento persistente para archivos y una estrategia de copias de seguridad.

## Comandos útiles

```bash
# Comprobar errores de configuración
python manage.py check

# Crear una nueva migración después de cambiar modelos
python manage.py makemigrations

# Aplicar migraciones pendientes
python manage.py migrate
```