@echo off
setlocal

echo ===================================================
echo   Uruchamianie Systemu QR ^& Barcode Generator
echo ===================================================
echo.

if not exist "backend\.env" (
    echo [INFO] Brak pliku backend\.env. Kopiowanie z backend\.env.example...
    copy "backend\.env.example" "backend\.env" >nul
    echo [INFO] Plik .env zostal utworzony.
) else (
    echo [INFO] Plik backend\.env juz istnieje.
)
echo.

echo [INFO] Budowanie obrazow i uruchamianie kontenerow w tle (Docker Compose)...
docker compose up --build -d

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [BŁĄD] Wystapil problem podczas uruchamiania Docker Compose!
    echo Upewnij sie, ze aplikacja Docker Desktop jest wlaczona.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [INFO] Oczekiwanie na pelna gotowosc bazy PostgreSQL i serwera FastAPI
timeout /t 5 /nobreak >nul
echo.

echo [INFO] Uruchamianie automatycznych testow pytest w kontenerze backendu...
docker compose exec web pytest tests/

echo.
echo ===================================================
echo [SUKCES] Proces zakonczony! Aplikacja jest gotowa.
echo.
echo - Interfejs uzytkownika (Frontend): http://localhost:5173
echo - Backend API:                      http://localhost:8000
echo - Dokumentacja API (Swagger):       http://localhost:8000/docs
echo ===================================================
echo.

pause