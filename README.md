# Readmates

Aplikacja społecznościowa dla pasjonatów książek, umożliwiająca dzielenie się recenzjami i przemyśleniami na temat przeczytanych lektur lub innych treści z szeroko pojętym czytelnictwem.

## Funkcjonalności

- **Rejestracja i logowanie**
- **Tworzenie postów** - tytuł posta, treść oraz możliwość wgrania zdjęcia
- **Feed z postami** – przeglądanie wszystkich postów z infinite scroll
- **Komentowanie** – dodawanie komentarzy do postów
- **Zapisywanie postów** – możliwość zapisywania interesujących postów do swojej biblioteczki dostępnej na profilu
- **Profil użytkownika** – widok własnych postów, zapisanych pozycji oraz statystyk (liczba postów, komentarzy)
- **Usuwanie postów** – możliwość usunięcia własnych publikacji
- **Obsługa błędów** – dedykowane strony dla błędów 404 i 500

## Dlaczego akurat Readmates?

Nie lubię mediów społecznościowych, jednak bardzo lubię kulturę, sztukę, rózne wydarzenia i właśnie między innymi - książki. Marzy mi się większa różnorodność platform społecznościowych, gdzie ludzie będą dzielić się swoimi pasjami bez wpadania w sidła algorytmów i złych praktyk projektowania zagarniających naszą uwagę. Tak pojawił się pomysł na Readmates, trochę taki Instagram, ale tylko o tematyce książkowej, który stawia pasję na pierwszym miejscu - zamiast kreacji, nieskazitelnego wizerunku czy statusu materialnego.

## Stack technologiczny

| Warstwa | Technologie |
|---------|-------------|
| Backend | Python 3, Flask |
| Baza danych | SQLAlchemy, SQLite |
| Formularze | Flask-WTF, WTForms |
| Frontend | Jinja2, Bootstrap 5, JavaScript |

## Jak uruchomić?

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/zuzannagasior/readmates.git
cd readmates
```

### 2. Utwórz i aktywuj wirtualne środowisko

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate     # Windows
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Uruchom aplikację

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: **http://127.0.0.1:5000**

## Testowy użytkownik

Do testowania aplikacji możesz użyć następujących danych logowania:

| Pole | Wartość |
|------|---------|
| Username | `czytelnik` |
| Hasło | `123456` |
