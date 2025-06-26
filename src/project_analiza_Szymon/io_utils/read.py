'''moduł do czytania danych z wejścia'''

import os
import pandas as pd

def load_data_from_folder(folder_path):
    '''ładowanie danych'''
    data_frames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            if filename == "powierzchnia_i_ludnosc_w_przekroju_" \
                           "terytorialnym_w_2024_roku_tablice.xlsx":
                file_path = os.path.join(folder_path, filename)
                print(f"Reading: {file_path}")
                pow_ludn_2024_woj = pd.read_excel(file_path, sheet_name = "Tabl. 1", skiprows=5)
                pow_ludn_2024_pow = pd.read_excel(file_path, sheet_name = "Tabl. 2", skiprows=2)
                data_frames.append((filename,pow_ludn_2024_woj))
                data_frames.append((filename, pow_ludn_2024_pow))
            elif filename == "nowe_mieszkania.xlsx":
                file_path = os.path.join(folder_path, filename)
                print(f"Reading: {file_path}")
                nowe_mieszk = pd.read_excel(file_path, sheet_name = "TABLICA", skiprows=2)
                data_frames.append((filename, nowe_mieszk))
            else:
                file_path = os.path.join(folder_path, filename)
                print(f"Reading: {file_path}")
                df = pd.read_excel(file_path)
                data_frames.append((filename, df))
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            print(f"Reading: {file_path}")
            df = pd.read_csv(file_path)
            data_frames.append((filename, df))
    return data_frames
