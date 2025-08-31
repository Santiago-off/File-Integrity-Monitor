🛡️ File Integrity Monitor

File Integrity Monitor es una herramienta desarrollada en Python para la monitorización de integridad de archivos.
Permite supervisar directorios críticos, calcular hashes SHA-256 y detectar modificaciones en tiempo real (creación, alteración o eliminación de archivos).

Este proyecto está diseñado como apoyo en entornos de ciberseguridad y auditoría, proporcionando trazabilidad y control sobre los cambios en el sistema de ficheros.

✨ Funcionalidades principales

Interfaz gráfica intuitiva con Tkinter.

Gestión de usuarios y roles (administrador / usuario estándar).

Escaneo de directorios vigilados con detección de:

Archivos añadidos.

Archivos modificados.

Archivos eliminados.

Historial de eventos y logs operativos almacenados en JSON.

Modo discreto mediante minimización en bandeja del sistema.

📂 Estructura del proyecto
📦Ciberseguridad
 ┣ 📜file_integrity_monitor.py   # Aplicación principal
 ┣ 📜run_integrity_monitor.bat   # Script de ejecución en Windows
 ┣ 📜file_hashes.json            # Base de datos de hashes calculados
 ┣ 📜watched_dirs.json           # Configuración de directorios vigilados
 ┣ 📜historial.json              # Historial de cambios registrados
 ┣ 📜logs.json                   # Registro de eventos operativos
 ┗ 📜users.json                  # Información de usuarios y roles

⚙️ Requisitos

Python 3.8+

Dependencias:

pip install pillow

▶️ Ejecución

Clonar el repositorio:

git clone https://github.com/tuusuario/Ciberseguridad.git
cd Ciberseguridad


Instalar dependencias:

pip install pillow


Ejecutar el programa con permisos de administrador:

run_integrity_monitor.bat

📌 Nota Importante

Este software se distribuye con fines educativos y de investigación en ciberseguridad.
Su uso en entornos de producción requiere una revisión y adaptación previa conforme a las políticas de seguridad de cada organización.
