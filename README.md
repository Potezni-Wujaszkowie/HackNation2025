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

## Narzędzie składa się z:

### 1. Dodawanie źródeł

Na pierwszym ekranie użytkownik może wprowadzić źródła informacji w dwóch formach:

1. Pliki

Obsługiwane formaty: .pdf, .docx

Po wgraniu pliku aplikacja automatycznie dokonuje ekstrakcji treści do postaci tekstowej.

2. Adresy URL

Użytkownik może podać URL jako źródło.

Aplikacja wykonuje rekurencyjne przeszukiwanie zawartości podanego adresu (wgłąb linków), pozyskując tekst wykorzystywany w późniejszych etapach.

### 2. Ekstrakcja, kompresja i budowa zbioru faktów

Po identyfikacji i przetworzeniu źródeł rozpoczyna się automatyczna analiza treści:
- Każde źródło zostaje skompresowane (tworzone są streszczenia o wysokiej gęstości informacji).
- Z tekstu wydobywane są fakty i kluczowe informacje, które następnie trafiają do zbioru faktów.

Użytkownik może:
- dodawać własne fakty,
- tworzyć założenia dotyczące przyszłości (modelowanie warunkowe),
- modyfikować wagi (istotność) poszczególnych faktów i założeń.

Mechanizm wag pozwala nadać różnym informacjom zróżnicowaną wartość w analizie końcowej.

### 3. Modelowanie i generowanie wyników

Po zdefiniowaniu zbioru faktów oraz ich wag dane trafiają do wybranego modelu analitycznego. Model ma zdefiniowany kontekst główny zadania, który kieruje analizą. Aplikacja tworzy dla modelu ważone streszczenia oraz przekazuje założenia zdefiniowane przez użytkownika. LLM działa w trybie agentowym (plan-and-solve), co pozwala mu:
- zaplanować strukturę analizy,
- wykonać logiczny, sekwencyjny tok rozumowania,
- wygenerować spójny i uargumentowany wynik.

Wynik końcowy obejmuje:
- streszczenie problemu,
- 4 scenariusze rozwoju sytuacji,
- 2 rekomendacje dla scenariusza pozytywnego i negatywnego.

Całość jest zgodna z formatem określonym w treści zadania głównego.

### Podsumowanie

Aplikacja umożliwia:
- automatyczne pozyskanie i analizę danych ze zróżnicowanych źródeł,
- budowę dynamicznego zbioru faktów i założeń,
- nadawanie im istotności,
- uruchomienie modelu LLM, który generuje strategiczne scenariusze oraz rekomendacje.

## Źródła wiedzy
- Przykładowe dane udostępnione przez autorów zadania
- Publicznie dostępne strony rządowe i organizacji międzynarodowych:
    - "https://www.nato.int/en/news-and-events/articles/news/2025/12/04/the-director-general-of-the-international-military-staff-discusses-nato-ukraine-cooperation-with-visiting-ukraine-military-personnel?selectedLocale="
    - "https://www.nato.int/en/news-and-events/articles/news/2025/11/26/nato-and-ukraine-announce-new-joint-initiative-to-accelerate-defence-innovation-unite-brave-nato?selectedLocale="
    - "https://www.nato.int/en/news-and-events/articles/news/2025/11/23/nato-deputy-secretary-general-visits-logistical-hub-in-poland-of-the-nato-security-assistance-and-training-for-ukraine?selectedLocale="
    - "https://www.nato.int/en/news-and-events/articles/news/2025/11/17/nato-allies-wrap-up-major-air-exercise-falcon-strike-2025-in-italy?selectedLocale="
    - "https://www.gov.pl/web/obrona-narodowa/bojowe-wozy-piechoty-borsuk-wchodza-na-wyposazenie-wojska-polskiego"
    - "https://www.gov.pl/web/obrona-narodowa/wspolpraca-na-rzecz-bezpieczenstwa-infrastruktury-krytycznej"
    - "https://www.gov.pl/web/premier/wspolna-deklaracja-podsumowujaca-polsko---niemieckie-konsultacje-miedzyrzadowe"
