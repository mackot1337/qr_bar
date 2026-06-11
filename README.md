# QR & Barcode Generator - Full-Stack Application

Kompletna aplikacja webowa służąca do zaawansowanego generowania spersonalizowanych kodów QR oraz kodów kreskowych. Projekt składa się z asynchronicznego backendu (FastAPI) połączonego z bazą danych PostgreSQL oraz responsywnego frontendowego interfejsu użytkownika (React + Vite).

Projekt został zrealizowany w ramach laboratorium z przedmiotu **„Języki skryptowe”** i spełnia wszystkie wymagania projektowe: separację warstw, zastosowanie wzorców SOLID i DRY, pełną konteneryzację, testy jednostkowe oraz czytelną dokumentację API.

Rozwiązuje on rzeczywisty problem, dostarczając użyteczne narzędzie, które może znaleźć zastosowanie w branży e-commerce, logistyce czy systemach biletowych (nie jest to wyłącznie demo technologiczne).

---

# Technologie i Zależności

Aplikacja została zbudowana przy użyciu nowoczesnego stosu technologicznego.

## Frontend

* **Framework:** React 19
* **Narzędzie budujące:** Vite 8
* **Komunikacja HTTP:** Axios
* **Stylizowanie:** CSS3

## Backend

* **Język:** Python 3.11
* **Framework WWW:** FastAPI
* **Baza danych:** PostgreSQL + SQLAlchemy
* **Przetwarzanie obrazu:** qrcode, python-barcode, Pillow
* **Testowanie:** pytest, httpx

## Infrastruktura

* Docker
* Docker Compose
* Bash

---

# Architektura i Zasady Projektowe

Projekt został zaprojektowany zgodnie z dobrymi praktykami programistycznymi.

## Separacja Warstw (Architektura Trójwarstwowa)

Ścisły podział na:

* **Frontend** – odpowiedzialny za prezentację danych i interakcję z użytkownikiem.
* **Logikę biznesową** – generatory kodów w `generators.py`.
* **Warstwę dostępu do danych** – pliki `models.py` i `database.py`.

## Zasady SOLID i DRY

Wykorzystano polimorfizm oraz klasy abstrakcyjne (`CodeGenerator`), aby uniknąć powielania kodu przy generowaniu różnych typów kodów graficznych. Rozwiązanie wspiera zasadę:

* Open/Closed Principle (OCP)
* Single Responsibility Principle (SRP)

## Automatyzacja Wdrożenia

Docker Compose odpowiada za orkiestrację trzech usług:

* `db`
* `web`
* `frontend`

Zapewnia to izolację środowiska oraz powtarzalność uruchomienia na różnych systemach operacyjnych.

## Testy Kontrolne

Pokrycie kluczowych funkcji generujących oraz endpointów HTTP testami automatycznymi (`pytest`) zwiększa stabilność projektu.

---

# 📂 Struktura Projektu

```text
qr_bar-frontend/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── generators.py
│   │   ├── main.py
│   │   └── models.py
│   ├── tests/
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── Dockerfile
│
├── docker-compose.yml
└── run.sh
```

---

# 🚀 Uruchomienie Projektu

## Wymagania Wstępne

Do uruchomienia aplikacji wymagane są:

* Docker
* Docker Compose
* Bash (Linux/macOS lub Git Bash/WSL na Windows) lub konsola Windowsa (CMD, Powershell)

---

## Opcja 1: Szybki Start (Zalecane)

Skrypt `run.sh` automatycznie:

* tworzy konfigurację środowiskową,
* buduje obrazy Dockera,
* uruchamia PostgreSQL,
* uruchamia backend i frontend,
* wykonuje testy kontrolne.

```bash
chmod +x run.sh
./run.sh

#Windows CMD
run.bat

#Windows Powershell
.\run.bat
```

---

## Opcja 2: Uruchomienie Ręczne (Docker)

### 1. Utwórz plik konfiguracyjny

```bash
cp backend/.env.example backend/.env
```

### 2. Zbuduj i uruchom kontenery

```bash
docker compose up --build -d
```

### 3. (Opcjonalnie) Uruchom testy

```bash
docker compose exec web pytest tests/
```

---

## Opcja 3: Uruchomienie Lokalne (Bez Dockera)

### Backend

Przejdź do katalogu backend:

```bash
python -m venv venv
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

Uruchom serwer:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

Przejdź do katalogu frontend:

```bash
npm install
npm run dev
```

---

# Jak poruszać się po aplikacji?

Po poprawnym uruchomieniu aplikacji cały system będzie dostępny lokalnie.

## 1. Interfejs Użytkownika (Frontend)

**Adres:**

```text
http://localhost:5173
```

Dostępne funkcje:

* Generowanie kodów QR z tekstu lub adresów URL.
* Generowanie kodów kreskowych.
* Obsługa standardów:

  * EAN-13
  * EAN-8
  * UPC-A
  * ISBN-13
  * Code128
* Personalizacja kolorów tła i wypełnienia.
* Dodawanie własnego logo do kodów QR.
* Historia wygenerowanych kodów.
* Pobieranie wcześniej utworzonych kodów.

---

## 2. Dokumentacja API (Swagger)

**Adres:**

```text
http://localhost:8000/docs
```

Swagger umożliwia:

* testowanie endpointów,
* walidację danych wejściowych,
* podgląd modeli żądań i odpowiedzi.

---

# Główne Endpointy API

## POST `/generate/qr`

Generowanie kodu QR.

### Parametry

```json
{
  "data": "https://example.com",
  "fill_color": "#000000",
  "back_color": "#ffffff",
  "logo_base64": "..."
}
```

---

## POST `/generate/barcode`

Generowanie kodu kreskowego.

### Parametry

```json
{
  "data": "5901234123457",
  "format": "ean13"
}
```

---

## GET `/history`

Pobieranie historii wygenerowanych kodów.

### Parametry Query

```text
skip=0
limit=20
```

Obsługuje paginację wyników.

---

# ✅ Najważniejsze Funkcjonalności

* Generowanie kodów QR.
* Generowanie kodów kreskowych.
* Personalizacja kolorów.
* Dodawanie logo do kodów QR.
* Historia generowanych kodów.
* API REST oparte o FastAPI.
* Automatyczna dokumentacja OpenAPI/Swagger.
* Testy jednostkowe i integracyjne.
* Pełna konteneryzacja przy użyciu Docker Compose.
* Architektura zgodna z zasadami SOLID i DRY.
