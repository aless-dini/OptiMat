"""
test_calculos.py
----------------
Pruebas de las funciones de calculos.py con un caso pequeño calculado a mano.

Ejecutar con:  python -m pytest
"""

import pytest

from calculos import (
    calcular_reposicion,
    calcular_costos,
    proyectar_demanda,
    detectar_riesgo_quiebre,
)

# Caso pequeño: 2 productos x 2 sucursales
CAPACIDAD = [[10, 20],
             [5, 8]]
STOCK = [[4, 15],
         [5, 2]]
TARIFAS = [100, 200]


def test_reposicion():
    # A mano: [[10-4, 20-15], [5-5, 8-2]] = [[6, 5], [0, 6]]
    resultado = calcular_reposicion(CAPACIDAD, STOCK)
    assert resultado.tolist() == [[6, 5], [0, 6]]


def test_costos():
    # A mano: producto 1 = 6*100 + 5*200 = 1600
    #         producto 2 = 0*100 + 6*200 = 1200
    #         total      = 1600 + 1200   = 2800
    reposicion = [[6, 5], [0, 6]]
    costos, total = calcular_costos(reposicion, TARIFAS)
    assert costos.tolist() == [1600, 1200]
    assert total == 2800


def test_proyectar_demanda():
    # A mano: (3 + 6 + 9) / 3 = 6   y   (10 + 20) / 2 = 15
    assert proyectar_demanda([[3, 6, 9], [10, 20]]) == [6.0, 15.0]


def test_riesgo_quiebre():
    # Stock total: producto 1 = 4 + 15 = 19, producto 2 = 5 + 2 = 7
    # Demanda: 20 y 7 -> producto 1 en riesgo (19 < 20), producto 2 no (7 no es < 7)
    assert detectar_riesgo_quiebre(STOCK, [20, 7]) == [True, False]


def test_errores_de_dimensiones():
    with pytest.raises(ValueError):
        calcular_reposicion([[1, 2]], [[1, 2, 3]])
    with pytest.raises(ValueError):
        calcular_costos([[1, 2]], [100, 200, 300])
    with pytest.raises(ValueError):
        detectar_riesgo_quiebre(STOCK, [1, 2, 3])
