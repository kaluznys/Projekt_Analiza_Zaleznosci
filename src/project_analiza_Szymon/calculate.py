'''moduł do obliczeń wykorzystywanych w analizie statystycznej'''
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

def simple_stat(array_val, array_arg):
    '''obliczanie prostych statystyk'''
    max_pow = array_val.max(), array_arg[array_val.argmax()]
    min_pow = array_val.min(), array_arg[array_val.argmin()]
    sred_pow = round(array_val.mean(), 2)
    med_pow = round(array_val.median(), 2)
    return (max_pow, min_pow, sred_pow, med_pow)

def regresja(x, y):
    '''przeprowadza regresję liniową'''
    x = np.array(x).reshape(-1,1)
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    return x, y_pred


def stat_wplyw_outlier(x, y):
    '''znajdowanie outlierów'''
    x = x.to_numpy()
    y = y.to_numpy()

    y_pred = regresja(x,y)[1]
    x_mean = x.mean()

    n=len(x)
    e = y-y_pred
    odch = x-x_mean
    h = 1/len(x)+odch**2/np.sum(odch**2)
    h = np.array(h, dtype=float)
    sigma = np.sqrt(1/(n-2)*sum(e**2))
    resid_stud = e/(sigma*np.sqrt(1-h))
    cook_dist = (resid_stud**2)*h/(2*(1-h))
    mask = (np.abs(resid_stud) > 2) & (cook_dist > 1)
    ind_wplyw_odst = np.where(mask)[0]
    return resid_stud, cook_dist, ind_wplyw_odst


def przyrosty_w_woj(ramka_2024, ramka_2023, nazwa_dane_2024, nazwa_dane_2023):
    '''badanie różnic w wartościach statystyk w kolejnych latach'''
    wspolna = pd.merge(ramka_2024, ramka_2023, on="Województwo")
    wspolna["przyrost"] = ramka_2024[nazwa_dane_2024] - ramka_2023[nazwa_dane_2023]
    return wspolna[["przyrost", "Województwo"]]
