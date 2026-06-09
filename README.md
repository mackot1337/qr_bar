# QR & Barcode Generator - Full-Stack Application

Kompletna aplikacja webowa służąca do zaawansowanego generowania spersonalizowanych kodów QR oraz kodów kreskowych. Projekt składa się z asynchronicznego backendu (FastAPI) połączonego z bazą danych PostgreSQL oraz responsywnego frontendowego interfejsu użytkownika (React + Vite).

Projekt został zrealizowany w ramach laboratorium z przedmiotu **"Języki skryptowe"** i spełnia wszystkie wymagania projektowe (separacja warstw, wzorce SOLID/DRY, konteneryzacja, testy jednostkowe oraz pełna dokumentacja).

## Struktura Całego Projektu

```text
qr_bar-frontend/
├── backend/            # Warstwa serwerowa (FastAPI, SQLAlchemy, Pytest)
│   ├── app/            # Logika biznesowa, endpointy i modele ORM
│   ├── tests/          # Testy jednostkowe i integracyjne
│   ├── Dockerfile      # Obraz dockera dla backendu
│   └── .env.example    # Szablon zmiennych środowiskowych bazy danych
├── frontend/           # Warstwa kliencka (React 19, Vite, Axios)
│   ├── src/            # Komponenty i style interfejsu UI
│   ├── public/         # Zasoby statyczne (ikony, favicon)
│   └── Dockerfile      # Obraz dockera dla frontendu (Zaktualizowany)
├── docker-compose.yml  # Główna konfiguracja wielokontenerowa (Full-Stack)
└── run.sh              # Skrypt automatyzujący uruchomienie całego systemu
```

## Wymagania Wstępne

Do uruchomienia aplikacji w najwygodniejszej, w pełni skonteneryzowanej wersji wymagane są:
* **Docker** oraz **Docker Compose**
* Terminal z powłoką typu Bash (Linux/macOS, lub Git Bash / WSL na systemie Windows)

## Szybkie Uruchomienie (Zalecane)

W głównym katalogu projektu znajduje się zaktualizowany skrypt `run.sh`. Automatycznie tworzy on konfigurację środowiskową, buduje obrazy Dockera dla frontendu i backendu, uruchamia bazę danych PostgreSQL, a na koniec przeprowadza automatyczną weryfikację poprawności backendu poprzez zestaw testów `pytest`.

Wykonaj w terminalu:
```bash
chmod +x run.sh
./run.sh
```

Po pomyślnym uruchomieniu aplikacja dostępna jest pod następującymi adresami:
* **Interfejs GUI (Frontend):** [http://localhost:5173](http://localhost:5173)
* **Backend API:** [http://localhost:8000](http://localhost:8000)
* **Interaktywna Dokumentacja API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

## Architektura i Spełnienie Zasad Projektowych

1. **Separacja Warstw:** Ścisły podział na niezależny Frontend (odpowiedzialny wyłącznie za prezentację danych i interakcję z użytkownikiem) oraz Backend (odpowiedzialny za logikę biznesową generowania kodów oraz trwałość danych).
2. **Zasady SOLID i DRY:** Wspólna abstrakcja dla generatorów graficznych (`CodeGenerator`), zamknięcie na modyfikacje i otwarcie na rozszerzenia (OCP), reużywalność modułów przetwarzania do formatu Base64.
3. **Automatyzacja Wdrożenia:** Wykorzystzenie Docker Compose do pełnej orkiestracji trzech usług (`db`, `web`, `frontend`) izoluje środowisko uruchomieniowe i gwarantuje powtarzalność na każdym systemie operacyjnym.
4. **Testy Kontrolne:** Pokrycie kluczowych funkcji generujących oraz endpointów HTTP testami automatycznymi gwarantuje stabilność prototypu.