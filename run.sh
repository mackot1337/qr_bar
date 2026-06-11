#!/bin/bash

echo "======================================================="
echo "   Uruchamianie Projektu: Generator Kodów QR i Kreskowych "
echo "======================================================="

if ! [ -x "$(command -v docker)" ]; then
  echo 'Błąd: Docker nie jest zainstalowany w systemie.' >&2
  exit 1
fi

if [ ! -f "backend/.env" ] && [ -f "backend/.env.example" ]; then
  echo "[0/3] Tworzenie pliku .env ze struktury szablonu..."
  cp backend/.env.example backend/.env
fi

echo "[1/3] Budowanie i uruchamianie kontenerów Full-Stack (Frontend + Backend + DB)..."
docker compose up --build -d

echo "[2/3] Oczekiwanie na uruchomienie i stabilizację usług..."
sleep 5

echo "[3/3] Uruchamianie testów automatycznych backendu..."
docker compose exec web pytest tests/

echo "======================================================="
echo " Sukces! Aplikacja jest gotowa:"
echo " - Frontend (React + Vite): http://localhost:5173"
echo " - Backend (FastAPI API):    http://localhost:8000"
echo " - Dokumentacja Swagger:     http://localhost:8000/docs"
echo "======================================================="