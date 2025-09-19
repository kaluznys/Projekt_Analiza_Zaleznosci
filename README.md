# projekt analizy danych - analiza_zalezności

Projekt ten dotyczy analizy zależności między różnymi zjawiskami takimi jak pożary, liczba ludności, mieszkalnictwo i zezwolenia na handel alkoholem.

---

## Opis

Projekt zawiera szereg potrzebnym funkcji i modułów do pracy z danymi. Jego działanie obejmuje między innymi:

- Wczytanie i wstępne przetwarzanie danych
- Eksploracyjną analizę danych
- Wizualizacje
- interpretację wyników
- Zapis danych do pliku
- Profiling projektu
- Testy

---
## Uruchamianie
1. Aby uruchomić plik główny należy, będąc w folderze głównym projektu wpisać w terminalu: py main.py --input_dir data (bądź python main.py --input_dir data). Wówczas uruchomiony zostanie kod przetwarzający dane, obliczający podstawowe statystyki i zapisujący je do pliku (domyślnie results).
2. Żeby uruchomić moduł z testami należy ponownie z folderu projektu wpisać w wierszu poleceń: pytest tests/
3. W celu obejrzenia głównej części projektu, czyli analizy w formie przejrzystego raportu zawierającej również profiling, należy wpisać z katalogu projektu: jupyter notebook (otwiera jupyter notebook, który musi być zainstalowany wcześniej przez użytkownika) a następnie otworzyć link, który się wyświetli oraz wybrać plik notebook_main.ipynb.


