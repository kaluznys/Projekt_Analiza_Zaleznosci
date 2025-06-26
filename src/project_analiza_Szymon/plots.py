'''moduł do tworzenia wizualizacji do intepretacji danych'''

import numpy as np
import matplotlib.pyplot as plt
from .calculate import regresja

def plot_regr_poz_lud(x,y):
    '''wykres regresji'''
    plt.scatter(x, y)
    plt.xlabel("Ludność ogółem")
    plt.ylabel("Pożary rok 2024")
    plt.title("Pożary względem liczby ludności")
    x_nowe, y_pred = regresja(x, y)
    plt.plot(x_nowe, y_pred, color='red', label='Regresja')
    plt.legend()

def plot_barplots(wojewodztwo, ludnosc, zezwolenia, pozary):
    '''tworzy trzy wykresy kolumnowe pod sobą'''
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(23, 9))

    axs[0].bar(wojewodztwo, ludnosc, color='violet')
    axs[0].set_title("liczba ludności")

    axs[1].bar(wojewodztwo, zezwolenia, color='blue')
    axs[1].set_title("zezwolenia")

    axs[2].bar(wojewodztwo, pozary, color='green')
    axs[2].set_title("pożary")

    plt.tight_layout()  # Avoid overlap
    plt.show()

def barplot_dwa(dana_1, dana_2, woj, os ="Województwa",\
                tytul = "Przyrosty (przeskalowane) w liczbie zezwoleń i pożarów",\
                legenda = ["przyrosty w zezwoleniach", "Przyrosty w pożarach"]):
    '''tworzy grupowany (po dwa słupki) wykres kolumnowy'''
    plt.figure(figsize=(25, 9))
    x = np.arange(16)

    width = 0.40
    y1 =dana_1
    y2 = dana_2
    ratio = y1.mean() / y2.mean()
    y2 *= abs(ratio)
    plt.bar(x - 0.2, y1, width)
    plt.bar(x + 0.2, y2, width)
    plt.xlabel(os)
    plt.title(tytul)
    plt.legend(legenda)
    plt.xticks(x, woj);
