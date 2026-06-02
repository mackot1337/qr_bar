#!/bin/bash

echo "======================================================="
echo "   Uruchamianie Generatora Kodów QR i Kreskowych       "
echo "======================================================="

if ! [ -x "$(command -v docker)" ]; then
  echo 'Błąd: Docker nie jest zainstalowany w systemie.' >&2
  exit 1
fi

echo "[1/3] Budowanie i uruchamianie kontenerów..."
docker compose up --build -d

echo "[2/3] Oczekiwanie na uruchomienie usług..."
sleep 3

echo "[3/3] Uruchamianie testów automatycznych..."
docker compose exec web pytest tests/

echo "======================================================="
echo " Sukces! Backend działa pod adresem: http://localhost:8000"
echo " Dokumentacja API (Swagger): http://localhost:8000/docs"
echo "======================================================="