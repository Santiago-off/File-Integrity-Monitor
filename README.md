🛡️ File Integrity Monitor
<p align="center"> <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python"/> <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"/> <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Platform"/> <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status"/> </p>

📖 Descripción

File Integrity Monitor es una herramienta de ciberseguridad en Python que supervisa directorios críticos, calcula hashes SHA-256 y registra cambios en los archivos (añadidos, modificados o eliminados).

Diseñada para entornos de auditoría y seguridad forense, ofrece trazabilidad completa y control de accesos por roles.


✨ Características

✅ Interfaz gráfica en Tkinter.

✅ Sistema de usuarios y roles (admin / usuario).

✅ Logs operativos e historial en JSON.

✅ Ejecución con permisos elevados.

✅ Modo discreto en bandeja del sistema.


📂 Estructura del proyecto

📦Ciberseguridad

 ┣ 📜file_integrity_monitor.py   # Aplicación principal
 
 ┣ 📜run_integrity_monitor.bat   # Script de ejecución
 
 ┣ 📜file_hashes.json            # Base de datos de hashes
 
 ┣ 📜watched_dirs.json           # Directorios vigilados
 
 ┣ 📜historial.json              # Historial de cambios
 
 ┣ 📜logs.json                   # Logs operativos
 
 ┗ 📜users.json                  # Usuarios y roles


⚙️ Tecnologías
Tecnología	Uso
Python 3.8+	Lenguaje principal
Tkinter	Interfaz gráfica
Pillow	Iconos en bandeja del sistema
JSON	Persistencia de datos


▶️ Instalación y uso

git clone https://github.com/Santiago-off/File-Integrity-Monitor.git

cd Ciberseguridad

pip install pillow

run_integrity_monitor.bat

⚠️ Nota

Este software se distribuye con fines educativos y de investigación en ciberseguridad.
Su implementación en producción debe realizarse con las debidas auditorías y revisiones de seguridad.
