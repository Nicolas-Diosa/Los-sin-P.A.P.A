#!/usr/bin/env bash
# ===============================================
# Script de configuración inicial del proyecto Django
# Versión para Linux / MacOS
# Autor: Equipo Los-sin-P.A.P.A
# ===============================================

# ---------- TÍTULO ----------
echo "==============================================="
echo "      🧩 Iniciando setup del proyecto Django"
echo "==============================================="

# ---------- 1. Levantar contenedor Docker ----------
echo ""
echo "🔹 Levantando base de datos PostgreSQL con Docker Compose..."

# Ejecuta docker compose moderno o clásico
docker compose up -d 2>/dev/null || docker-compose up -d

echo "⏳ Esperando que el contenedor se inicie..."
sleep 5

# ---------- 2. Variables de entorno ----------
echo ""
echo "🔹 Configurando variables de entorno..."

DB_USER="usuario"
DB_NAME="parchate"
CONTAINER_NAME="postgres_server"
INIT_SQL="Proyecto/Backend/cmd/bd/init.sql"

# ---------- 3. Ejecutar script SQL de inicialización ----------
echo ""
if [ -f "$INIT_SQL" ]; then
  echo "🔹 Ejecutando script SQL de inicialización..."
  docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" < "$INIT_SQL"
else
  echo "⚠️  No se encontró el archivo $INIT_SQL, se omite esta parte."
fi

# ---------- 4. Instalar dependencias ----------
echo ""
echo "🔹 Creando entorno virtual e instalando dependencias..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ---------- 5. Migraciones iniciales ----------
echo ""
echo "🔹 Aplicando migraciones a la base de datos..."
python manage.py migrate

# ---------- 6. Pruebas básicas (placeholder) ----------
echo ""
echo "🔹 Ejecutando pruebas básicas..."
python manage.py check

# ---------- 7. Mensaje final ----------
echo ""
echo "✅ Setup completado correctamente."
echo "Ejecuta ahora: python manage.py runserver"
echo "==============================================="