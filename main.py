'''skrypt przeprowadzający obliczenia prostych statystych dla analizowanych
danych i zapisanie ich do odpowiedniego pliku podanego z terminala'''
import argparse

from src.project_analiza_Szymon.io_utils.read import load_data_from_folder
import src.project_analiza_Szymon.preprocessing as prep
from src.project_analiza_Szymon.io_utils.write import writing_stats

def main():
    '''główna funkcja'''
    parser = argparse.ArgumentParser(description="Final assignment data loader")
    parser.add_argument(
        "--input_dir",
        type=str,
        required=True,
        help="Path to directory containing CSV files."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="output.txt",
        help="Path to save results."
    )
    args = parser.parse_args()

    datasets = load_data_from_folder(args.input_dir)
    print(datasets)

    pozary_grup_pw = prep.pozary_powiat(datasets[0][1])
    ludn_pow_2024_pow = prep.ludn_powiat(datasets[3][1])
    koncesje_hurt = prep.koncesje(datasets[5][1])

    df_ludn_poz = prep.lacz_ludn_pozar(ludn_pow_2024_pow, pozary_grup_pw)


    pozary, ludnosc,  zezwolenia, poz_lud_powiat, zez_wojewodztwo = \
        df_ludn_poz["Ludność ogółem"],df_ludn_poz["Pożary rok 2024"],\
        koncesje_hurt["liczba_zezwolen"], df_ludn_poz.powiat,koncesje_hurt["Województwo"]

    writing_stats(args.output_file, pozary, ludnosc, zezwolenia, poz_lud_powiat, zez_wojewodztwo)

if __name__ == "__main__":
    main()
