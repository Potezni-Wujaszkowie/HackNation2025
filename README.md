# HackNation2025


Repozytorium projektu HackNation2025 zawiera rozwiązanie zadania SCENARIUSZE JUTRA dla Ministerstwa Spraw Zagranicznych RP w ramach Hackathonu HackNation2025.

## Autorzy
- Błażej Ejzak
- Paweł Dombrzalski
- Bartosz Jaśinski
- Łukasz Wójcicki

## Opis projektu

Narzędzie realizuje zadania eksploracji danych politycznych, geopolitycznych i społecznych z różnych źródeł wskazancyh przez autorów zadania. Wykorzystuje techniki przetwarzania języka naturalnego (NLP) do analizy tekstów, udostępnie interfejs użytkownika umożliwiający komunikacje z narzedzieniem.

# HackNation2025


Repozytorium projektu HackNation2025 zawiera rozwiązanie zadania SCENARIUSZE JUTRA dla Ministerstwa Spraw Zagranicznych RP w ramach Hackathonu HackNation2025.

## Autorzy
- Błażej Ejzak
- Paweł Dombrzalski
- Bartosz Jaśinski
- Łukasz Wójcicki

## Opis projektu

Narzędzie realizuje zadania eksploracji danych politycznych, geopolitycznych i społecznych z różnych źródeł wskazancyh przez autorów zadania. Wykorzystuje techniki przetwarzania języka naturalnego (NLP) do analizy tekstów, udostępnie interfejs użytkownika umożliwiający komunikacje z narzedzieniem.

## Uruchomienie projektu
Do uruchomienia potrzebny jest pakiet [uv](https://docs.astral.sh/uv/). Uruchomienie aplikacji:
```shell
uv run frontend/runner.py
```

## Użyte technologie
- Python
- uv
- streamlit
- Gemini API
- PLLuM
- Beautiful Soup 4
- sqlite
- loguru

## Źródła wiedzy
- Przykładowe dane udostępnione przez autorów zadania
- Publicznie dostępne strony rządowe i organizacji międzynarodowych:

legit_urls = [
    "https://www.nato.int/en/news-and-events/articles/news/2025/12/04/the-director-general-of-the-international-military-staff-discusses-nato-ukraine-cooperation-with-visiting-ukraine-military-personnel?selectedLocale="
    , "https://www.nato.int/en/news-and-events/articles/news/2025/11/26/nato-and-ukraine-announce-new-joint-initiative-to-accelerate-defence-innovation-unite-brave-nato?selectedLocale="
    , "https://www.nato.int/en/news-and-events/articles/news/2025/11/23/nato-deputy-secretary-general-visits-logistical-hub-in-poland-of-the-nato-security-assistance-and-training-for-ukraine?selectedLocale="
    , "https://www.nato.int/en/news-and-events/articles/news/2025/11/17/nato-allies-wrap-up-major-air-exercise-falcon-strike-2025-in-italy?selectedLocale="
    , "https://www.gov.pl/web/obrona-narodowa/bojowe-wozy-piechoty-borsuk-wchodza-na-wyposazenie-wojska-polskiego"
    , "https://www.gov.pl/web/obrona-narodowa/wspolpraca-na-rzecz-bezpieczenstwa-infrastruktury-krytycznej"
    , "https://www.gov.pl/web/premier/wspolna-deklaracja-podsumowujaca-polsko---niemieckie-konsultacje-miedzyrzadowe"
]
