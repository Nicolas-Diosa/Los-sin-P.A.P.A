#!/usr/bin/env bash
set -euo pipefail

# Django Project Setup Script (Linux / macOS)
# Replica de la lógica de setup.bat: crear/leer .env, levantar docker, ejecutar init.sql,
# crear/activar venv en Proyecto e instalar dependencias.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Iniciando setup del proyecto..."

# Si no existe .env, crear uno por defecto (cambiar si siempre existe)
if [ ! -f "$SCRIPT_DIR/.env" ]; then
  echo "Creando archivo .env predeterminado..."
  cat > "$SCRIPT_DIR/.env" <<'EOF'
# .env file
POSTGRES_USER=usuario
POSTGRES_PASSWORD=passwordsegura
POSTGRES_DB=parchate
POSTGRES_CONTAINER_NAME=postgres_server
POSTGRES_PORT=0811
EOF
  echo "Archivo .env creado exitosamente."
else
  echo ".env ya existe, no se realizaron cambios."
fi

# Cargar variables desde .env
echo "Cargando variables desde .env..."
# Leer línea por línea, ignorar comentarios y líneas vacías
while IFS='=' read -r key value; do
  # Trim whitespace from key
  key_trimmed="$(echo "$key" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  if [ -z "$key_trimmed" ]; then
    continue
  fi
  # ignorar comentarios
  case "$key_trimmed" in
    \#*) continue ;;
  esac
  # value: remove leading spaces
  value_trimmed="$(echo "${value:-}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  # quitar comillas envolventes si existen
  value_trimmed="$(echo "$value_trimmed" | sed -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/")"
  # exportar la variable
  export "$key_trimmed=$value_trimmed"
done < <(grep -v '^\s*$' "$SCRIPT_DIR/.env")

# Mapear variables internas
: "${POSTGRES_USER:=usuario}"
: "${POSTGRES_DB:=parchate}"
: "${POSTGRES_CONTAINER_NAME:=postgres_server}"
DB_USER="${POSTGRES_USER}"
DB_NAME="${POSTGRES_DB}"
CONTAINER_NAME="${POSTGRES_CONTAINER_NAME}"

echo "POSTGRES_USER=$POSTGRES_USER"
echo "POSTGRES_DB=$POSTGRES_DB"
echo "POSTGRES_CONTAINER_NAME=$POSTGRES_CONTAINER_NAME"
echo "DB_USER=$DB_USER"
echo "DB_NAME=$DB_NAME"
echo "CONTAINER_NAME=$CONTAINER_NAME"

# Levantar PostgreSQL con Docker Compose
echo "Levantando PostgreSQL con Docker Compose..."
if ! docker compose up -d; then
  echo "Intento fallido con 'docker compose', probando con 'docker-compose'..."
  docker-compose up -d
fi

echo "Cargando..."
sleep 5

# Ejecutar el script SQL de inicialización si existe
INIT_SQL="$SCRIPT_DIR/Proyecto/Backend/cmd/bd/init.sql"
if [ -f "$INIT_SQL" ]; then
  echo "Ejecutando script SQL de inicialización..."
  # usar cat | docker exec -i para alimentar stdin de psql
  cat "$INIT_SQL" | docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME"
else
  echo "No se encontró $INIT_SQL"
fi

# Crear y activar entorno virtual dentro de Proyecto
echo "Creando/activando entorno virtual en Proyecto..."
pushd "$SCRIPT_DIR/Proyecto" >/dev/null

if [ ! -d "venv" ]; then
  echo "Creando venv con 'python3 -m venv venv'..."
  if ! python3 -m venv venv; then
    echo "Error creando venv con 'python3', intentando con 'python'..."
    python -m venv venv
  fi
else
  echo "Ya existe la carpeta venv, no se creará una nueva."
fi

echo "Activando entorno virtual..."
# shellcheck disable=SC1091
source venv/bin/activate

echo "Instalando paquetes pip..."
python -m pip install --upgrade pip
python -m pip install django psycopg2-binary python-dotenv pytest pytest-django flake8

popd >/dev/null

echo
echo "Setup completado."

exit 0

