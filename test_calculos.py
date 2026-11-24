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
    verificar_despacho,
    proyectar_demanda,
    detectar_riesgo_quiebre,
)

# Caso pequeño: 2 productos x 2 clientes
PEDIDOS = [[10, 20],
           [5, 8]]
ENTREGADO = [[4, 15],
             [5, 2]]
TARIFAS = [100, 200]


def test_reposicion():
    # A mano: [[10-4, 20-15], [5-5, 8-2]] = [[6, 5], [0, 6]]
    resultado = calcular_reposicion(PEDIDOS, ENTREGADO)
    assert resultado.tolist() == [[6, 5], [0, 6]]


def test_costos():
    # A mano: producto 1 = 6*100 + 5*200 = 1600
    #         producto 2 = 0*100 + 6*200 = 1200
    #         total      = 1600 + 1200   = 2800
    reposicion = [[6, 5], [0, 6]]
    costos, total = calcular_costos(reposicion, TARIFAS)
    assert costos.tolist() == [1600, 1200]
    assert total == 2800


def test_verificar_despacho():
    # Pendiente: producto 1 = 6 + 5 = 11, producto 2 = 0 + 6 = 6
    # Bodega: 8 y 10 -> faltan 11 - 8 = 3 del producto 1; el producto 2 alcanza (0)
    total, faltantes = verificar_despacho([8, 10], [[6, 5], [0, 6]])
    assert total.tolist() == [11, 6]
    assert faltantes.tolist() == [3, 0]


def test_proyectar_demanda():
    # A mano: (3 + 6 + 9) / 3 = 6   y   (10 + 20) / 2 = 15
    assert proyectar_demanda([[3, 6, 9], [10, 20]]) == [6.0, 15.0]


def test_riesgo_quiebre():
    # Bodega 19 y 7; demanda 20 y 7 -> producto 1 en riesgo (19 < 20), producto 2 no
    assert detectar_riesgo_quiebre([19, 7], [20, 7]) == [True, False]


def test_errores_de_dimensiones():
    with pytest.raises(ValueError):
        calcular_reposicion([[1, 2]], [[1, 2, 3]])
    with pytest.raises(ValueError):
        calcular_reposicion([[1, 2]], [[5, 2]])  # entregado mayor que pedido
    with pytest.raises(ValueError):
        calcular_costos([[1, 2]], [100, 200, 300])
    with pytest.raises(ValueError):
        verificar_despacho([1, 2, 3], [[1, 2]])
    with pytest.raises(ValueError):
        detectar_riesgo_quiebre([1, 2], [1, 2, 3])


# ---------------- Arreglo de 3 dimensiones, semaforo y grafico ----------------

from calculos import resumir_ventas, calcular_cobertura, clasificar_alertas


def test_resumir_ventas():
    # 2 productos x 2 clientes x 3 meses
    ventas = [
        [[1, 2, 3],     # producto 1, cliente 1
         [4, 5, 6]],    # producto 1, cliente 2
        [[0, 1, 0],     # producto 2, cliente 1
         [2, 2, 2]],    # producto 2, cliente 2
    ]
    por_mes, por_cliente = resumir_ventas(ventas)
    # A mano, sumando los clientes: producto 1 = [1+4, 2+5, 3+6] = [5, 7, 9]
    #                               producto 2 = [0+2, 1+2, 0+2] = [2, 3, 2]
    assert por_mes.tolist() == [[5, 7, 9], [2, 3, 2]]
    # A mano, sumando los meses: producto 1 = [1+2+3, 4+5+6] = [6, 15]
    #                            producto 2 = [0+1+0, 2+2+2] = [1, 6]
    assert por_cliente.tolist() == [[6, 15], [1, 6]]


def test_resumir_ventas_exige_3_dimensiones():
    with pytest.raises(ValueError):
        resumir_ventas([[1, 2, 3], [4, 5, 6]])


def test_cobertura():
    # Demanda 30 al mes = 1 por dia -> 15 unidades alcanzan 15 dias.
    # Demanda 60 al mes = 2 por dia -> 90 unidades alcanzan 45 dias.
    assert calcular_cobertura([15, 90], [30, 60]) == [15.0, 45.0]
    # Sin demanda, el stock no se agota
    assert calcular_cobertura([5], [0]) == [float("inf")]


def test_clasificar_alertas_en_los_bordes():
    # 30 es verde; 29.9 y 20 son amarillo; 19.9 es rojo
    assert clasificar_alertas([30, 29.9, 20, 19.9]) == ["VERDE", "AMARILLO", "AMARILLO", "ROJO"]
    with pytest.raises(ValueError):
        clasificar_alertas([10], umbral_verde=20, umbral_amarillo=30)


def test_grafico_de_alertas(tmp_path):
    from graficos import graficar_alertas
    archivo = tmp_path / "alertas.png"
    graficar_alertas(["A", "B", "C"], [40, 25, 10], ["VERDE", "AMARILLO", "ROJO"], archivo=str(archivo))
    assert archivo.exists() and archivo.stat().st_size > 0
