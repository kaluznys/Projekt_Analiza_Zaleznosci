"testowanie funkcji do obliczeń"
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),\
                                                '..',"..", 'Projekt_Analiza_Zaleznosci')))

from src.project_analiza_Szymon.calculate import *

def test_simple_stat():
    arr_val = pd.Series([1, 2, 3, 4, 5])
    arr_arg = pd.Series([10, 20, 30, 40, 50])
    result = simple_stat(arr_val, arr_arg)

    # max_pow = (max_value, arg_max)
    assert result[0] == (5, 50)
    # min_pow = (min_value, arg_min)
    assert result[1] == (1, 10)
    # średnia
    assert result[2] == 3.0
    # mediana
    assert result[3] == 3.0


def test_regresja():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    x_out, y_pred = regresja(x, y)

    assert x_out.shape == (5, 1)
    # Gdyż y=2*x, przewidywania powinny być bardzo bliskie oryginałowi y
    np.testing.assert_allclose(y_pred, y, atol=1e-6)


def test_stat_wplyw_outlier():
    # Przygotuj dane z outlierem
    x = pd.Series([1, 2, 3, 4, 5, 100])
    y = pd.Series([2, 4, 6, 8, 10, 300])

    resid_stud, cook_dist, ind_outlier = stat_wplyw_outlier(x, y)

    assert resid_stud.shape == x.shape
    assert cook_dist.shape == x.shape

    assert 5 in ind_outlier


def test_przyrosty_w_woj():
    ramka_2024 = pd.DataFrame({
        "Województwo": ["A", "B", "C"],
        "dane2024": [10, 20, 30]
    })
    ramka_2023 = pd.DataFrame({
        "Województwo": ["A", "B", "C"],
        "dane2023": [5, 15, 25]
    })
    wynik = przyrosty_w_woj(ramka_2024, ramka_2023, "dane2024", "dane2023")

    assert list(wynik.columns) == ["przyrost", "Województwo"]

    expected = [5, 5, 5]
    assert all(wynik["przyrost"] == expected)
