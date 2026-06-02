# QR & Barcode Generator API - Backend

Backendowa część aplikacji do zaawansowanego generowania spersonalizowanych kodów QR oraz kodów kreskowych. Projekt został zrealizowany w ramach laboratorium z przedmiotu **"Języki skryptowe"**.

Aplikacja udostępnia interfejs API (oparty na **FastAPI**), z którym komunikuje się frontend. Pozwala na szybkie generowanie kodów, personalizację kolorów, osadzanie logotypów w kodach QR oraz zapisywanie historii wygenerowanych kodów w bazie danych **PostgreSQL**.

## Realizacja założeń projektowych
Projekt został zaprojektowany z zachowaniem dobrych praktyk programistycznych i wprost odpowiada na wymagania laboratoryjne:
- **Rozwiązanie rzeczywistego problemu:** Zapewnia użyteczne narzędzie np. dla branży e-commerce, logistyki czy systemów biletowych (nie jest to tylko demo technologiczne).
- **Separacja warstw (architektura trójwarstwowa):** Oddzielono logikę biznesową (generatory w `generators.py`) od warstwy dostępu do danych (`models.py`, `database.py`) oraz endpointów HTTP (`main.py`).
- **Zasady SOLID i DRY:** Wykorzystano m.in. polimorfizm i klasy abstrakcyjne (`CodeGenerator`), aby uniknąć powielania kodu przy generowaniu różnych typów kodów graficznych.
- **Testowanie jednostkowe:** Krytyczne funkcje aplikacji oraz endpointy są dokładnie przetestowane przy pomocy frameworka `pytest`.
- **Wdrożenie i pakiety:** Środowisko aplikacji jest w pełni zautomatyzowane dzięki wykorzystaniu kontenerów **Docker** i skryptu powłoki.

## Technologie
- **Język:** Python 3.11
- **Framework WWW:** FastAPI (nowoczesny, asynchroniczny z automatyczną dokumentacją OpenAPI)
- **Baza Danych:** PostgreSQL + SQLAlchemy (narzędzie ORM)
- **Przetwarzanie obrazu i kodów:** `qrcode`, `python-barcode`, `Pillow`
- **Testy automatyczne:** `pytest`, `httpx`
- **Infrastruktura:** Docker, Docker Compose, skrypt Bash (`run.sh`)

## Struktura projektu
```text
backend/
├── app/
│   ├── config.py       # Konfiguracja bazująca na zmiennych środowiskowych (Pydantic)
│   ├── database.py     # Inicjalizacja połączenia z bazą danych
│   ├── generators.py   # Logika biznesowa - generowanie kodów QR i kreskowych
│   ├── main.py         # Definicja aplikacji FastAPI i głównych endpointów
│   └── models.py       # Modele ORM (tabele w bazie np. CodeHistory)
├── tests/
│   ├── test_generators.py # Testy jednostkowe logiki biznesowej
│   └── test_main.py       # Testy integracyjne API
├── .env.example        # Szablon zmiennych środowiskowych
├── docker-compose.yml  # Definicja usług kontenerowych (web, db)
├── Dockerfile          # Konfiguracja obrazu backendu
├── requirements.txt    # Definicja paczek i zależności Pythona
└── run.sh              # Skrypt automatyzujący budowę i testy
```

## Uruchomienie projektu

### Wymagania wstępne
Aby uruchomić projekt, system musi posiadać:
* **Docker** oraz **Docker Compose**
* Terminal z powłoką typu bash (Linux/macOS, w Windowsie np. Git Bash / WSL)

### Opcja 1: Szybki start
W projekcie znajduje się skrypt `run.sh`, który samodzielnie upewnia się o obecności Dockera, buduje obrazy, odpala kontenery (w tym bazę danych) i od razu uruchamia zestaw testów automatycznych.

W terminalu wpisz:
```bash
chmod +x run.sh
./run.sh
```

### Opcja 2: Uruchomienie ręczne (Docker)
Jeśli wolisz mieć pełną kontrolę krok po kroku:

1. Skopiuj i w razie potrzeby dostosuj plik ze zmiennymi środowiskowymi:
   ```bash
   cp .env.example .env
   ```
2. Uruchom środowisko w tle
    ```bash
    docker compose up --build -d
    ```
3. Zweryfikuj poprawność działania aplikacji poprzez uruchomienie testów (opcjonalne):
    ```bash
    docker compose exec web pytest tests/
    ```

### Opcja 3: Uruchomienie lokalne (bez Dockera)

1. Utwórz i aktywuj wirtualne środowisko Pythona:
    ```bash
    python -m venv venv
    source venv/bin/activate  # W systemie Windows użyj: venv\Scripts\activate
    ```
2. Zainstaluj zależności:
    ```bash
    pip install -r requirements.txt
    ```
3. Skonfiguruj bazę danych. Zmień DATABASE_URL w pliku .env na bazę z której korzystasz lokalnie (np. na sqlite:///./test.db do szybkiego testu).
4. Uruchom serwer developerski:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

## Dokumentacja API (Swagger)

Jedną z największych zalet FastAPI jest auto-generowana dokumentacja interaktywna. Po poprawnym uruchomieniu aplikacji (lokalnie lub w Dockerze), wejdź w przeglądarce na adres:

**[http://localhost:8000/docs](http://localhost:8000/docs)**

Znajdziesz tam wizualny interfejs, w którym możesz testować wszystkie poniższe ścieżki:

### Dostępne Endpointy
* **`POST /generate/qr`** - Tworzy kod QR. Możesz przesłać żądany kolor wypełnienia, kolor tła oraz opcjonalnie ciąg `logo_base64`, aby osadzić logotyp na środku kodu.
* **`POST /generate/barcode`** - Tworzy kod kreskowy. Obsługuje m.in. standardy `code128`, `code39`, `ean13`, `ean8`, `isbn13`, `upca`.
* **`GET /history`** - Pobiera stronicowaną listę (parametry `skip` i `limit`) wygenerowanych wcześniej kodów zachowanych w bazie.