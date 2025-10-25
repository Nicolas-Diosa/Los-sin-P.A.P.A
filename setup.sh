# TODO: Verificar si el .env ya existe, si no, crearlo.

# Título de la ventana (solo decorativo en Linux)
echo "     Django Project Setup Script"

# Levantamiento de la Base de Datos con Docker Compose
echo "Levantando PostgreSQL con Docker Compose..."
docker compose up -d

# Si el anterior comando falló, intentar con la versión antigua
if [ $? -ne 0 ]; then
    echo "Intento fallido con 'docker compose', probando con 'docker-compose'..."
    docker-compose up -d
fi

# Esperar (5 segundos)
echo "Cargando..."
sleep 5

# Ejecutar el script SQL de inicialización
# Asegurarse de que estas variables coincidan con el .env
DB_USER="usuario"
DB_NAME="parchate"
CONTAINER_NAME="postgres_server"

if [ -f "Proyecto/Backend/cmd/bd/init.sql" ]; then
    echo "Ejecutando script SQL de inicialización..."
    docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" < "Proyecto/Backend/cmd/bd/init.sql"
else
    echo "No se encontró Proyecto/Backend/cmd/bd/init.sql"
fi

# TODO: Descargar dependencias de Python
# pip install -r requirements.txt

echo
cd ../..
echo "Setup completado."
