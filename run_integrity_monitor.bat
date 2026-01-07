@echo off
setlocal
:: Cambiar el directorio de trabajo a la carpeta donde reside este archivo .bat
cd /d "%~dp0"
title FIM Installer & Runner

:: 1. Verificar privilegios de Administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Por favor, ejecuta este archivo como ADMINISTRADOR.
    pause
    exit /b
)

echo ====================================================
echo      FILE INTEGRITY MONITOR - AUTO-PATH CONFIG
echo ====================================================

:: 2. Verificar si Python está instalado
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Python no se encuentra instalado en el sistema.
    start https://www.python.org/downloads/
    pause
    exit /b
)

:: 3. Instalar dependencias
echo [*] Verificando dependencias en: %cd%
python -m pip install pystray Pillow >nul

:: 4. Crear users.json si no existe
if not exist "users.json" (
    echo [{"username": "admin", "password": "admin123", "role": "admin"}] > users.json
)

:: 5. Ejecutar la aplicacion usando la ruta absoluta detectada
echo [*] Ruta detectada: %~dp0file_integrity_monitor.py
echo [*] Iniciando monitor...

python "%~dp0file_integrity_monitor.py"

if %errorLevel% neq 0 (
    echo [ERROR] Hubo un problema al iniciar el programa.
    echo Revisa que el archivo 'file_integrity_monitor.py' este en la misma carpeta que este .bat.
    pause
)