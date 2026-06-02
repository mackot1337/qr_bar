# API do Generowania Kodów QR i Kreskowych

Projekt zrealizowany w ramach laboratorium z przedmiotu "Języki skryptowe". Jest to backendowa część aplikacji służącej do generowania spersonalizowanych kodów QR oraz kodów kreskowych, stworzona z myślą o integracji z frontendem w React.

## Architektura i Technologie
* **Framework API:** FastAPI (Python 3.11)
* **Baza danych:** PostgreSQL (SQLAlchemy)
* **Generowanie kodów:** Biblioteki `qrcode` oraz `python-barcode`
* **Infrastruktura:** Docker & Docker Compose
* **Testy:** Pytest

Struktura projektu oddziela logikę biznesową (`service`) od obsługi żądań HTTP (katalog `main`) i warstwy danych (`models` i `database`). Zastosowano abstrakcję dla generatorów kodów, co pozwala na łatwe dodawanie nowych formatów w przyszłości.

## Wymagania wstępne
Aby uruchomić projekt, potrzebujesz zainstalowanego w systemie:
* **Docker** oraz **Docker Compose**

## Uruchomienie projektu

Do projektu dołączony jest skrypt automatyzujący wdrożenie (budowanie obrazów, uruchamianie bazy danych i aplikacji oraz odpalanie testów).

W systemach Linux/macOS uruchom w terminalu:
```bash
./run.sh
