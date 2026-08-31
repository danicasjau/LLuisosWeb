@echo off
title AE Lluïsos de Gràcia - Web Server
echo ======================================================
echo   Iniciant servidor web - AE Lluïsos de Gràcia
echo ======================================================
echo.

:: Comprova si hi ha un entorn virtual existent i l'activa
if exist .venv\Scripts\activate.bat (
    echo Activant entorn virtual (.venv)...
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    echo Activant entorn virtual (venv)...
    call venv\Scripts\activate.bat
)

echo Executant aplicacio: python app.py...
echo.
python app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ======================================================
    echo [ERROR] S'ha produit un error en executar l'aplicacio.
    echo Assegura't de tenir Python instal·lat i les dependències:
    echo   pip install -r requirements.txt
    echo ======================================================
    pause
)
