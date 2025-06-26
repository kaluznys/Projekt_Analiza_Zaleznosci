'''testy kompletności danych'''
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
EXPECTED_FILES = {'C1.xlsx', 'nowe_mieszkania.xlsx',\
                  'powierzchnia_i_ludnosc_w_przekroju_terytorialnym_w_2024_roku_tablice.xlsx',\
                  'raport_na_dzien_1_września_2023_r.csv',\
                  'raport_zezwoleń_czynnych_na_dzień_2_września_2024_r.csv'}

def test_data_directory_exists():
    '''sprawdza, czy folder z danymi istnieje'''
    assert os.path.isdir(DATA_DIR), f"Katalog {DATA_DIR} nie istnieje"

def test_expected_files_exist():
    '''czy zawiera potrzebne dane'''
    existing_files = set(os.listdir(DATA_DIR))
    missing = EXPECTED_FILES - existing_files
    assert not missing, f"Brakuje plików: {missing}"

def test_no_unexpected_files():
    '''czy nie zawiera niepotrzebnych plików'''
    existing_files = set(os.listdir(DATA_DIR))
    unexpected = existing_files - EXPECTED_FILES
    assert not unexpected, f"Nieoczekiwane pliki: {unexpected}"
