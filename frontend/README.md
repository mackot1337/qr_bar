# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
# QR & Barcode Generator - Frontend Interface

Ta część projektu stanowi graficzny interfejs użytkownika (GUI) dla generatora kodów QR oraz kodów kreskowych. Została zbudowana przy użyciu nowoczesnego stacku technologicznego skupionego wokół biblioteki **React**.

Interfejs komunikuje się asynchronicznie z serwerem (FastAPI) za pomocą klienta HTTP **Axios**, przesyłając parametry personalizacji kodów i odbierając gotowe obrazy w formacie tekstowym Base64, które są natychmiast renderowane na ekranie.

## Technologie i Biblioteki

* **Framework bazowy:** React 19 (najnowsza specyfikacja)
* **Narzędzie deweloperskie / Bundler:** Vite 8 (zapewniające błyskawiczne przeładowywanie kodu HMR)
* **Komunikacja HTTP:** Axios (obsługa żądań asynchronicznych POST/GET)
* **Stylizowanie:** Czysty CSS3 z obsługą zmiennych środowiskowych dla trybu jasnego/ciemnego (*Light/Dark mode*)

## Funkcjonalności GUI

* **Wprowadzanie danych:** Dynamiczne pole tekstowe na adresy URL, numery seryjne lub dowolne teksty (obsługa do 2000 znaków).
* **Przełącznik trybu:** Intuicyjny wybór pomiędzy generowaniem kodu QR a tradycyjnym kodem kreskowym.
* **Personalizacja kolorów:** Dwa próbniki kolorów (Fill Color / Back Color) połączone z natywnym systemowym paletnikiem.
* **Wgrywanie Logo (Opcja QR):** Możliwość zaimportowania pliku graficznego, który zostanie przekonwertowany na Base64 i zintegrowany z wygenerowanym kodem QR.
* **Obsługa Błędów:** Czytelne komunikaty walidacyjne w przypadku problemów z połączeniem lub podania błędnych parametrów.

## Uruchomienie Lokalne (Bez Dockera)

Jeśli chcesz uruchomić frontend bezpośrednio na swoim systemie (wymagane środowisko **Node.js** w wersji 18 lub nowszej):

1. Wejdź do katalogu frontendu:
   ```bash
   cd frontend
   ```
2. Zainstaluj wymagane zależności z pliku `package.json`:
   ```bash
   npm install
   ```
3. Uruchom lokalny serwer deweloperski:
   ```bash
   npm run dev
   ```
4. Otwórz w przeglądarce adres podany w konsoli (domyślnie `http://localhost:5173`).