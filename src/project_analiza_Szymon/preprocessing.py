'''moduł, który zawiera przetwarzanie danych umożliwiające dalszą analizę
 przy pomocy m.in. modułów calculate i plots'''

import pandas as pd


def ludn_powiat(ludn_pow_2024_pow):
    '''ramka dot. ludności w powiatach'''
    # usunięcie kolumn po nazwach
    col_ind_names = [ludn_pow_2024_pow.columns[i] for i in [0, 2, -3, -2, -1]]
    ludn_pow_2024_pow = ludn_pow_2024_pow.drop(col_ind_names, axis=1)
    # zmiana nazw
    ludn_pow_2024_pow.columns = ['powiaty', 'powierzchnia w km^2',\
                                'Ludność ogółem', "Ludność na km^2"]
    print(f"w danych są przerwy np. {ludn_pow_2024_pow.head()}")
    # usuń przerwy, trzeba uważać na spacje
    tab_bool = ~ludn_pow_2024_pow.isin(
        {'powiaty': [" Powiaty:", " Powiats:", " Miasta na prawach powiatu:",\
                     ' Cities with powiat status:']})
    ludn_pow_2024_pow = ludn_pow_2024_pow[tab_bool]
    ludn_pow_2024_pow = ludn_pow_2024_pow[~ludn_pow_2024_pow.powiaty.isna()]
    print(f'liczby braków w kol.: {ludn_pow_2024_pow.isna().sum()}')
    print("braki są w tych samych wierszach: ")
    ludn_pow_2024_pow = ludn_pow_2024_pow.reset_index(drop=True)
    powierzchnia = ludn_pow_2024_pow.loc[:, 'powierzchnia w km^2']
    na_indices = powierzchnia[powierzchnia.isna()].index
    print(f"powierzchnia : {na_indices}")
    ludn = ludn_pow_2024_pow.loc[:, 'Ludność ogółem']
    na_indices = ludn[ludn.isna()].index
    print(f"ludnosc ogolem: {na_indices}")
    ludn_km = ludn_pow_2024_pow.loc[:, 'Ludność na km^2']
    na_indices = ludn_km[ludn_km.isna()].index
    print(f"Ludność na km^2 : {na_indices}")
    #usuwanie braków
    print(ludn_pow_2024_pow.iloc[na_indices, :])
    ludn_pow_2024_pow = ludn_pow_2024_pow.drop(na_indices, axis=0)
    ludn_pow_2024_pow = ludn_pow_2024_pow.reset_index(drop=True)
    # teraz nie ma braków
    print(f'brak na\n{ludn_pow_2024_pow.isna().sum()}')
    # spacje na pocz.
    ludn_pow_2024_pow = ludn_pow_2024_pow.rename(columns={'powiaty': 'powiat'})
    ludn_pow_2024_pow['powiat'] = ludn_pow_2024_pow['powiat'].str.strip()
    return ludn_pow_2024_pow
def koncesje(koncesje_hurt):
    '''dane o liczbie zezwoleń na handel alkoholem'''
    koncesje_hurt1 = koncesje_hurt.groupby(['Województwo']).count()
    koncesje_hurt1 = koncesje_hurt1.iloc[:, 0:1]

    # indeksowanie
    koncesje_hurt1["Województwo"] = koncesje_hurt1.index
    koncesje_hurt1.index = list(range(len(koncesje_hurt1['Województwo'])))
    # string
    koncesje_hurt1 = koncesje_hurt1.rename(columns={'Numer zezwolenia': 'liczba_zezwolen'})
    koncesje_hurt1['Województwo'] = koncesje_hurt1['Województwo']\
        .str.replace('WOJ. ', '', regex=False).str.lower()
    print(f'brak na\n {koncesje_hurt1.isna().sum()}')
    return koncesje_hurt1
def pozary_powiat(pozary_liczba):
    '''ramka o pożarach w powiatach'''
    # wybór kol
    pozary_liczba = pozary_liczba.iloc[:, [1, 2, 5, 7, 9]]
    # grupowanie po powiatach dla liczb zdarzeń
    pozary_grup_pw = pozary_liczba.groupby(['Powiat']).sum()
    pozary_grup_pw["powiat"] = pozary_grup_pw.index
    pozary_grup_pw = pozary_grup_pw.drop("Województwo", axis=1).reset_index(drop=True)
    print(f'brak na\n {pozary_grup_pw.isna().sum()}')
    return pozary_grup_pw
def ludn_woj(lud_pow_woj):
    '''ramka dot. ludności w województwach'''
    col_ind_names = [lud_pow_woj.columns[i] for i in [0, 2, -3, -2, -1]]
    lud_pow_woj = lud_pow_woj.drop(col_ind_names, axis=1)
    lud_pow_woj.columns = ['Województwo', 'powierzchnia w km^2',\
                           'Ludność ogółem', "Ludność na km^2"]
    lud_pow_woj['Województwo'] = lud_pow_woj['Województwo'].str.lower()
    print(f'brak na\n {lud_pow_woj.isna().sum()}')
    return lud_pow_woj
def pozary_woj(pozary_liczba):
    '''ramka o pożarach w województwach'''
    pozary_liczba = pozary_liczba.iloc[:, [1, 2, 5, 7, 9]]
    # grupowanie po powiatach dla liczb zdarzeń
    pozary_grup_woj = pozary_liczba.groupby(['Województwo']).sum()
    pozary_grup_woj["Województwo"] = pozary_grup_woj.index
    pozary_grup_woj = pozary_grup_woj.drop("Powiat", axis=1).reset_index(drop=True)
    print(f'brak na\n {pozary_grup_woj.isna().sum()}')
    return pozary_grup_woj
def lacz_ludn_pozar(ludn_pow_2024_pow, pozary_grup_pw):
    '''dane dot. powiatów jednocześnie o ludności i pożarach'''
    df_ludn_poz = pd.merge(ludn_pow_2024_pow, pozary_grup_pw, on='powiat', how='outer')
    print(f'sprawdźmy ile danych straciliśmy przy łączeniu: {df_ludn_poz.isna().sum()}\n '
          f'sprawdźmy które obserwacje z ramek za to odpowiadają')
    na_ind = df_ludn_poz["Ludność ogółem"][df_ludn_poz["Ludność ogółem"].isna()].index
    na_ind2 = df_ludn_poz["Pożary rok 2024"][df_ludn_poz["Pożary rok 2024"].isna()].index
    print(df_ludn_poz.iloc[na_ind, :], df_ludn_poz.iloc[na_ind2, :])
    print('poprawmy, ten sam powiat')
    ludn_pow_2024_pow.loc[ludn_pow_2024_pow['powiat'] == 'm. st. Warszawa', 'powiat'] = 'Warszawa'
    df_ludn_poz = pd.merge(ludn_pow_2024_pow, pozary_grup_pw, on='powiat', how='outer')
    print(f'braki: {df_ludn_poz.isna().sum()}')
    return df_ludn_poz
def lacz_trzy(df_1, df_2, df_3):
    '''łączy trzy ramki o województwach'''
    df_merged = pd.merge(df_1, df_2, on='Województwo', how='outer')
    df_merged = pd.merge(df_merged, df_3, on='Województwo', how='outer')
    print(f'braki: {df_merged.isna().sum()}')
    return df_merged
def pozary_wczesniej(pozary_liczba):
    '''zwraca ramkę o liczbach pożarów we wcześniejszym (2023) roku'''
    pozary_liczba = pozary_liczba.loc[:, ["Województwo", "Pożary rok 2023"]]
    pozary_2023 = pozary_liczba.groupby(['Województwo']).sum()
    pozary_2023["Województwo"] = pozary_2023.index
    pozary_2023 = pozary_2023.reset_index(drop=True)
    print(f'brak na\n {pozary_2023.isna().sum()}')
    return pozary_2023
def nowe_mieszkania(mieszk):
    '''ramka o liczbie oddanych mieszkań w ostanich latach'''
    mieszk = mieszk.iloc[2:, 1:]
    mieszk = mieszk[["Unnamed: 1", "2023", "2024"]]
    mieszk.columns = ["Województwo", "nowe_mieszkania_2023", "nowe_mieszkania_2024"]
    mieszk = mieszk[mieszk['Województwo'].str.isupper()].reset_index(drop=True)
    mieszk['Województwo'] = mieszk['Województwo'].str.lower()

    print(f"Są wszystkie woj: {len(mieszk['Województwo'])}")
    print(f'brak na\n {mieszk.isna().sum()}')
    return  mieszk
