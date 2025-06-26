'''testy wczytywania i zapisu danych'''
import sys
import os
import pandas as pd
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),\
                                                '..',"..", 'my_project')))
from src.project_analiza_Szymon.io_utils.read import load_data_from_folder
from src.project_analiza_Szymon.io_utils.write import writing_stats

def mock_simple_stat(values, regions):
    '''funkcja symulująca simple_stats z calculate dla konkretnych danych'''
    return (30, 'C'), (10, 'A'), 20.0, 20.0

def test_writing_stats_creates_output(tmp_path):
    '''test wpisywania odpowiednich informacji'''
    df = pd.DataFrame({
        'powiat': ['A', 'B', 'C'],
        'wartosc': [10, 20, 30]
    })

    output_file = tmp_path / "output.txt"

    with patch("src.project_analiza_Szymon.io_utils.write.simple_stat",\
               side_effect=mock_simple_stat):
        writing_stats(
            output_file,
            df['wartosc'], df['wartosc'], df['wartosc'],
            df['powiat'], df['powiat']
        )

    content = output_file.read_text(encoding='utf-8-sig')

    assert "najwięcej pożarów (liczba, powiat): 30, C" in content
    assert "największa ludność" in content
    assert "min, średnia i mediana liczby zezwoleń: 10, 20.0, 20.0" in content

def test_load_data_from_folder_csv(tmp_path):
    '''test ładowania danych z plików csv'''
    # sztuczny plik tymczasowy
    sample_csv = tmp_path / "sample.csv"
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    df.to_csv(sample_csv, index=False)

    result = load_data_from_folder(tmp_path)

    assert len(result) == 1
    assert result[0][0] == "sample.csv"
    pd.testing.assert_frame_equal(result[0][1], df)

def test_load_data_from_folder_xlsx(tmp_path):
    '''test ładowania danych z plików .xlsx bez dodatkowych ustawień'''
    sample_xlsx = tmp_path / "test.xlsx"
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df.to_excel(sample_xlsx, index=False)

    result = load_data_from_folder(tmp_path)

    assert len(result) == 1
    assert result[0][0] == "test.xlsx"
    pd.testing.assert_frame_equal(result[0][1], df)

def test_wczytaj_dane_specjalne(tmp_path):
    '''test ładowania danych .xlsx, które wymagały sprecyzowanych parametrów'''
    test_file1 = tmp_path / "nowe_mieszkania.xlsx"
    test_file2 = tmp_path / 'powierzchnia_i_ludnosc_w_przekroju_terytorialnym_w_2024_roku_tablice.xlsx'

    dane_skip5 = [
        ["NAGŁÓWEK NIEPOTRZEBNY"],
        ["INNY WSTĘP"],
        ["jakieś niepotrzebne"],
        ["przerwa"],
        ["Kol1", "Kol2"],
        [1, 10],
        [2, 20]
    ]
    dane_skip2 = [
        ["NAGŁÓWEK NIEPOTRZEBNY"],
        ['kolum1', 'kolum2'],
        ["pierwszy", 100],
        ["drugi", 200]
    ]

    df_skip5 = pd.DataFrame(dane_skip5)
    df_skip2 = pd.DataFrame(dane_skip2)

    with pd.ExcelWriter(test_file2, engine='xlsxwriter') as writer:
        df_skip5.to_excel(writer, sheet_name='Tabl. 1', index=False)
        df_skip2.to_excel(writer, sheet_name='Tabl. 2', index=False)

    df_skip2.to_excel(test_file1, sheet_name = "TABLICA", index=False)

    result = load_data_from_folder(tmp_path)

    df_skip5_expect = pd.DataFrame({'Kol1': [1, 2], 'Kol2': [10, 20]})

    df_skip2_expect = pd.DataFrame({'kolum1': ["pierwszy", "drugi"], 'kolum2': [100, 200]}
)
    print(result[1][1])
    print("drug")
    print(df_skip2_expect)
    assert result[0][0] == 'nowe_mieszkania.xlsx', "zła ścieżka pliku"
    assert result[1][0] == \
           "powierzchnia_i_ludnosc_w_przekroju_terytorialnym_w_2024_roku_tablice.xlsx","zła nazwa pliku"

    try:
        pd.testing.assert_frame_equal(result[0][1].reset_index(drop="T"), df_skip2_expect)
    except AssertionError as e:
        raise AssertionError("ramka 1 niepoprawna") from e
    try:
        pd.testing.assert_frame_equal(result[1][1], df_skip5_expect)
    except AssertionError as e:
        raise AssertionError("ramka 2 niepoprawna") from e
    try:
        pd.testing.assert_frame_equal(result[2][1], df_skip2_expect)
    except AssertionError as e:
        raise AssertionError("ramka 3 niepoprawna") from e
