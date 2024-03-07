# Sistema de Control de Inventarios

Sistema de Control de Inventarios
Este proyecto es un sistema de control de inventarios desarrollado en FastAPI con base de datos MySQL, que permite gestionar el inventario de una empresa, así como la administración de usuarios con diferentes roles.

Características principales
Gestión de inventario: Permite añadir, editar y eliminar productos del inventario.
Roles de usuario: Define diferentes roles de usuario (administrador, gerente, empleado) con diferentes permisos.
Autenticación segura: Utiliza JWT para autenticar usuarios y proteger las rutas según los roles.
Instalación
Clona este repositorio: git clone https://github.com/NCYT30/inventario.git
Instala las dependencias: pip install -r requirements.txt
Configura la base de datos MySQL en el archivo config.py.
Ejecuta las migraciones: python main.py migrate
Ejecuta la aplicación: uvicorn main:app --reload
Uso
Accede a la aplicación en tu navegador: http://localhost:8000
Inicia sesión con las credenciales de usuario.
Explora las diferentes funcionalidades según tu rol de usuario.
