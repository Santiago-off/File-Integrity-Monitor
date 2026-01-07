🛡️ File Integrity Monitor (FIM) - Pro Console
<p align="center"> <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python"/> <img src="https://img.shields.io/badge/UI-Custom_Dark_Mode-blueviolet.svg" alt="UI"/> <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Platform"/> <img src="https://img.shields.io/badge/Security-SHA--256-red.svg" alt="Security"/> </p>

📖 Descripción
File Integrity Monitor es una solución avanzada de ciberseguridad diseñada para la vigilancia proactiva de sistemas de archivos. Utiliza criptografía SHA-256 para generar firmas digitales únicas de cada archivo, permitiendo detectar cualquier alteración, intrusión o borrado accidental en tiempo real.

Con una interfaz inspirada en centros de operaciones de seguridad (SOC), esta herramienta es ideal para administradores de sistemas que requieren un control estricto sobre directorios críticos.

✨ Características Premium
🖥️ Dashboard de Alto Impacto: Interfaz profesional en modo oscuro de 1200x750px optimizada para legibilidad.

🔍 Análisis Universal: Capacidad de reconocer y auditar archivos comprimidos (.rar, .zip), ejecutables, imágenes y carpetas completas.

📊 Identificación Detallada: Tabla de integridad que vincula cada Hash SHA-256 con su nombre de archivo correspondiente.

⚠️ Alertas Inteligentes: Notificaciones visuales intuitivas que detallan el número exacto de archivos Añadidos, Eliminados y Modificados.

👤 Control de Acceso (RBAC): Sistema de login seguro con gestión de permisos basada en roles.

📥 Auto-Instalador: Script .bat inteligente que configura rutas, verifica dependencias y solicita permisos de administrador automáticamente.

📂 Estructura del Proyecto
📦 File-Integrity-Monitor
 ┣ 📜 file_integrity_monitor.py   # Núcleo de la aplicación (UI + Motor de Hash)
 ┣ 📜 run_integrity_monitor.bat   # Launcher inteligente y gestor de dependencias
 ┣ 📜 file_hashes.json            # Base de datos de firmas digitales
 ┣ 📜 watched_dirs.json           # Registro de rutas bajo vigilancia
 ┣ 📜 historial.json              # Registro cronológico de alertas detectadas
 ┣ 📜 users.json                  # Credenciales cifradas y roles
 ┗ 📜 logs.json                   # Auditoría de eventos del sistema

⚙️ Tecnologías y Requisitos
 Tecnología,Propósito
        Python 3.8+,Motor de ejecución principal.
        Tkinter (Custom),Interfaz de usuario de alta fidelidad.
        Pystray & Pillow,Gestión del icono en la bandeja del sistema (System Tray).
        Hashlib,Generación de firmas criptográficas SHA-256.

▶️ Instalación Rápida (Plug & Play)
No necesitas configurar variables de entorno manualmente. El sistema está diseñado para ser ejecutado con un solo clic:

Clonar el repositorio:
git clone https://github.com/Santiago-off/File-Integrity-Monitor.git
cd File-Integrity-Monitor

Ejecutar: Haz clic derecho sobre run_integrity_monitor.bat y selecciona "Ejecutar como administrador".

[!TIP] El script instalará automáticamente las librerías necesarias (Pillow, pystray) y configurará el usuario administrador inicial si es la primera vez que se ejecuta.

🔐 Credenciales por Defecto
Usuario: admin

Contraseña: admin123

⚠️ Nota Legal: Este software se distribuye con fines educativos y de auditoría. Asegúrese de tener autorización antes de monitorear sistemas de terceros.