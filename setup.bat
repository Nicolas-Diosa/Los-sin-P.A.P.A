@echo off
:: Titilo de la ventana
title Django Project Setup Script

:: Print
echo  Iniciando setup del proyecto...
echo.

:: Levantamiento de la Base de Datos con Docker Compose
echo Levantando PostgreSQL con Docker Compose...
docker compose up -d

:: Si el anterior comando fallo, intentar con la version antigua
IF %ERRORLEVEL% NEQ 0 (
    echo Intento fallido con 'docker compose', probando con 'docker-compose'...
    docker-compose up -d
)

:: Esperar
echo Cargando...
timeout /t 5 /nobreak > NUL

:: Ejecutar el script SQL de inicialización
:: Asegurarse de que estas variables coincidan con el .env 
set DB_USER=usuario
set DB_NAME=parchate
set CONTAINER_NAME=postgres_server

IF EXIST "Proyecto\Backend\cmd\bd\init.sql" (
    echo Ejecutando script SQL de inicialización...
    type "Proyecto\Backend\cmd\bd\init.sql" | docker exec -i %CONTAINER_NAME% psql -U %DB_USER% -d %DB_NAME%
) ELSE (
    echo No se encontró Proyecto\Backend\cmd\bd\init.sql
)

echo.

cd ..\..

echo  Setup completado.

:EOF