import os
from waitress import serve
from mapavivo.wsgi import application

if __name__ == '__main__':
    # El puerto será asignado dinámicamente por IIS.
    port = int(os.environ.get('HTTP_PLATFORM_PORT', 8000))
    # Inicia el servidor Waitress
    serve(application, host='127.0.0.1', port=port)