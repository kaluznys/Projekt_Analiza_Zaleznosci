'''zapisywanie podstawowych danych do zadanego pliku'''
from ..calculate import simple_stat

def writing_stats(output_file, pozary, ludnosc,  zezwolenia, poz_lud_powiat,zez_wojewodztwo):
    with open(output_file, 'w', encoding='utf-8-sig') as output:
        output.write(
            f'najwięcej pożarów (liczba, powiat): '
            f'{simple_stat(pozary, poz_lud_powiat)[0][0]}, '
            f'{simple_stat(pozary, poz_lud_powiat)[0][1]}\n')
        output.write(
            f'największa ludność (liczba, powiat): '
            f'{simple_stat(ludnosc, poz_lud_powiat)[0][0]}, '
            f'{simple_stat(ludnosc, poz_lud_powiat)[0][1]}\n')
        output.write(
            f'najwięcej koncesji (liczba, województwo): '
            f'{simple_stat(zezwolenia, zez_wojewodztwo)[0][0]}, '
            f'{simple_stat(zezwolenia, zez_wojewodztwo)[0][1]}\n')
        output.write(
            f'min, średnia i mediana liczby pożarów: '
            f'{simple_stat(pozary, poz_lud_powiat)[1][0]}, '
            f'{simple_stat(pozary, poz_lud_powiat)[2]}, '
            f'{simple_stat(pozary, poz_lud_powiat)[3]}\n')
        output.write(
            f'min, średnia i mediana liczby ludności: '
            f'{simple_stat(ludnosc, poz_lud_powiat)[1][0]}, '
            f'{simple_stat(ludnosc, poz_lud_powiat)[2]}, '
            f'{simple_stat(ludnosc, poz_lud_powiat)[3]}\n')
        output.write(
            f'min, średnia i mediana liczby zezwoleń: '
            f'{simple_stat(zezwolenia, zez_wojewodztwo)[1][0]}, '
            f'{simple_stat(zezwolenia, zez_wojewodztwo)[2]}, '
            f'{simple_stat(zezwolenia, poz_lud_powiat)[3]}\n')
