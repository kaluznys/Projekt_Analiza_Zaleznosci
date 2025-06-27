'''testowanie przetwarzania danych'''
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),\
                                                '..',"..", 'analiza_zaleznosci')))

from src.project_analiza_Szymon.preprocessing import *

def test_ludn_powiat():

    df = pd.DataFrame({
        'zbedne1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'potrzebna1': [' Powiaty:', " Powiats:", ' Cities with powiat status:', \
                       " Miasta na prawach powiatu:", None,\
                       ' a', ' b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'],
        'zbedne2': range(16),
        'potrzebna2': range(16),
        'potrzebna3': range(16),
        'potrzebna4': range(16),
        'zbedne3': range(16),
        'zbedne4': range(16),
        'zbedne5': range(16)
    })


    df.loc[15, ['potrzebna2', 'potrzebna3', 'potrzebna4']] = None
    print(df)
    result = ludn_powiat(df)

    df_expect = pd.DataFrame({
        'powiat': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
        'powierzchnia w km^2': [float(i) for i in range(5,15)],
        'Ludność ogółem': [float(i) for i in range(5,15)],
        'Ludność na km^2': [float(i) for i in range(5,15)]
    })

    assert list(result.columns) == ['powiat', 'powierzchnia w km^2',\
                                    'Ludność ogółem', 'Ludność na km^2']
    # Sprawdź, że nie ma już wartości filtrujących
    assert not result['powiat'].isin(
        [" Powiaty:", " Powiats:", " Miasta na prawach powiatu:",\
         ' Cities with powiat status:']).any()
    # Brak wartości null w kolumnach
    assert not result.isna().any().any()
    pd.testing.assert_frame_equal(result, df_expect)

def test_koncesje():
    df = pd.DataFrame({
        'Województwo': ['WOJ. A', 'WOJ. B', 'WOJ. A', 'WOJ. C'],
        'Numer zezwolenia': [1, 2, 3, 4]
    })
    result = koncesje(df)
    # Powinno być 3 wiersze (dla A,B,C)
    assert result.shape[0] == 3
    # Kolumny: liczba_zezwolen, Województwo
    assert 'liczba_zezwolen' in result.columns
    assert 'Województwo' in result.columns
    # Sprawdź, że województwa są lowercase i bez "WOJ. "
    assert all(result['Województwo'].str.islower())
    assert all(~result['Województwo'].str.contains("WOJ."))

def test_pozary_powiat():
    df = pd.DataFrame({
        "col0" : [0 , 0, 0 ,0],
        'Województwo': ['A', 'A', 'B', 'B'],
        'Powiat': ['p1', 'p1', 'p2', 'p2'],
        'col3': [1, 2, 3, 4],
        'col4': [5, 6, 7, 8],
        'col5': [9, 10, 11, 12],
        'col6': [13, 14, 15, 16],
        'col7': [17, 18, 19, 20],
        'col8': [21, 22, 23, 24],
        'col9': [25, 26, 27, 28],
        'col10': [29, 30, 31, 32]
    })
    # Funkcja wybiera kolumny [1, 2, 5, 7, 9] -> 'Województwo', 'Powiat', 'col6', 'col8', 'col10'
    result = pozary_powiat(df)
    # Powinny zostać pogrupowane po Powiat
    assert 'powiat' in result.columns
    # Liczba unikalnych powiatów
    assert result.shape[0] == len(df['Powiat'].unique())
    # Brak kolumny 'Województwo'
    assert 'Województwo' not in result.columns


def test_ludn_woj():

    df = pd.DataFrame({
        'zbedne1': [1, 2, 3, 4],
        'potrzebna1': ["MAZOWIECKIE", "ŚLĄSKIE", 'WIELKOPOLSKIE', "MAŁOPOLSKIE"],
        'zbedne2': range(4),
        'potrzebna2': range(4),
        'potrzebna3': range(4),
        'potrzebna4': range(4),
        'zbedne3': range(4),
        'zbedne4': range(4),
        'zbedne5': range(4)
    })
    result = ludn_woj(df)
    result: pd.DataFrame
    assert list(result.columns) == ['Województwo', 'powierzchnia w km^2',\
                                    'Ludność ogółem', 'Ludność na km^2']
    # Województwa lowercase
    assert all(result['Województwo'].str.islower())

def test_pozary_woj():
    df = pd.DataFrame({
        "col0": [0, 0, 0, 0],
        'Województwo': ['A', 'A', 'B', 'B'],
        'Powiat': ['p1', 'p1', 'p2', 'p2'],
        'col3': [1, 2, 3, 4],
        'col4': [5, 6, 7, 8],
        'col5': [9, 10, 11, 12],
        'col6': [13, 14, 15, 16],
        'col7': [17, 18, 19, 20],
        'col8': [21, 22, 23, 24],
        'col9': [25, 26, 27, 28],
        'col10': [29, 30, 31, 32]
    })
    result = pozary_woj(df)
    assert 'Województwo' in result.columns
    assert 'Powiat' not in result.columns
    # Liczba unikalnych województw
    assert result.shape[0] == len(df['Województwo'].unique())


def test_lacz_ludn_pozar():
    ludn = pd.DataFrame({
        'powiat': ['a', 'b', 'm. st. Warszawa'],
        'Ludność ogółem': [1000, 2000, 3000],
        'powierzchnia w km^2': [10, 20, 30],
        'Ludność na km^2': [100, 200, 300]
    })
    pozary = pd.DataFrame({
        'powiat': ['a', 'b', 'Warszawa'],
        'Pożary rok 2024': [5, 10, 15],
        'col': [0, 0, 0]
    })
    result = lacz_ludn_pozar(ludn.copy(), pozary)
    # Sprawdź czy w wyniku jest kolumna "Pożary rok 2024"
    assert 'Pożary rok 2024' in result.columns
    # Powinny być połączone na podstawie powiatów (z poprawką na Warszawa)
    assert 'Warszawa' in result['powiat'].values


def test_lacz_trzy():
    df1 = pd.DataFrame({'Województwo': ['a', 'b'], 'val1': [1, 2]})
    df2 = pd.DataFrame({'Województwo': ['a', 'b'], 'val2': [3, 4]})
    df3 = pd.DataFrame({'Województwo': ['a', 'b'], 'val3': [5, 6]})
    result = lacz_trzy(df1, df2, df3)
    # Sprawdź kolumny
    assert all(col in result.columns for col in ['val1', 'val2', 'val3'])
    assert result.shape[0] == 2

def test_pozary_wczesniej():
    df = pd.DataFrame({
        'Województwo': ['A', 'A', 'B', 'B'],
        'Pożary rok 2023': [1, 2, 3, 4],
        'Inna kol': [5, 6, 7, 8]
    })
    result = pozary_wczesniej(df)
    assert 'Województwo' in result.columns
    assert 'Pożary rok 2023' in result.columns
    assert list(result['Pożary rok 2023']) == [3, 7]
    assert result.shape[0] == len(df['Województwo'].unique())

def test_nowe_mieszkania():
    df = pd.DataFrame({
        "col0" : range(6),
        "Unnamed: 1": ["X", "Y", "WIELKOPOLSKIE", "MAZOWIECKIE", "Dolnośląskie", "ŚLĄSKIE"],
        "2023": [0, 0, 100, 200, 300, 400],
        "2024": [0, 0, 110, 210, 310, 410],
        "zbedna": range(6)
    })
    result = nowe_mieszkania(df)
    # Sprawdź, że tylko wiersze gdzie województwo jest uppercase (tu 3 wiersze)
    assert set(result['Województwo']) == {'wielkopolskie', 'mazowieckie', "śląskie"}
    assert all(col in result.columns for col in \
               ['Województwo', 'nowe_mieszkania_2023', 'nowe_mieszkania_2024'])
