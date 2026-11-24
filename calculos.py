"""
calculos.py
-----------
Funciones matematicas de OptiMat.

Todas las funciones son "puras": reciben datos, devuelven un resultado
y no imprimen nada ni modifican variables globales.
"""

import numpy as np


def calcular_reposicion(capacidad, stock):
    """
    Calcula la matriz de reposicion (RESTA DE MATRICES).

    Formula:  R = C - S
    donde C es la matriz de capacidad maxima y S la matriz de stock actual.
    Cada elemento R[i][j] indica cuantas unidades del producto i hay que
    enviar a la sucursal j para dejarla llena.

    Parametros:
        capacidad: matriz (lista de listas o arreglo NumPy) productos x sucursales.
        stock: matriz con las mismas dimensiones que capacidad.

    Retorna:
        Arreglo NumPy con la matriz de reposicion.
    """
    matriz_capacidad = np.array(capacidad)
    matriz_stock = np.array(stock)

    # Para restar dos matrices deben tener el mismo tamaño
    if matriz_capacidad.shape != matriz_stock.shape:
        raise ValueError(
            f"Las matrices de capacidad {matriz_capacidad.shape} y de stock "
            f"{matriz_stock.shape} deben tener las mismas dimensiones."
        )

    # El stock no puede superar la capacidad (daria una reposicion negativa)
    if np.any(matriz_stock > matriz_capacidad):
        raise ValueError("Hay stock mayor que la capacidad maxima en alguna sucursal.")

    # Resta elemento a elemento
    reposicion = matriz_capacidad - matriz_stock
    return reposicion


def calcular_costos(reposicion, tarifas):
    """
    Calcula el costo de despacho (PRODUCTO MATRIZ x VECTOR).

    Formula:  costos = R * t
    donde R es la matriz de reposicion (productos x sucursales) y t es el
    vector de tarifas por unidad (una tarifa por sucursal).
    Cada componente del resultado es:
        costos[i] = R[i][0]*t[0] + R[i][1]*t[1] + ... (costo del producto i)

    El costo logistico total es la suma de todas las componentes del vector.

    Parametros:
        reposicion: matriz productos x sucursales.
        tarifas: vector con una tarifa por sucursal (columna).

    Retorna:
        Una tupla (vector_costos, costo_total).
    """
    matriz_reposicion = np.array(reposicion)
    vector_tarifas = np.array(tarifas)

    # La cantidad de columnas de la matriz debe ser igual al largo del vector
    if matriz_reposicion.shape[1] != vector_tarifas.shape[0]:
        raise ValueError(
            f"La matriz de reposicion tiene {matriz_reposicion.shape[1]} sucursales "
            f"(columnas), pero el vector de tarifas tiene {vector_tarifas.shape[0]} valores."
        )

    # Producto matriz por vector
    vector_costos = matriz_reposicion @ vector_tarifas

    # Suma de las componentes del vector = costo total
    costo_total = vector_costos.sum()
    return vector_costos, costo_total


def proyectar_demanda(historial_ventas):
    """
    Proyecta la demanda de cada producto como el promedio de sus ventas
    (SUMATORIA).

    Formula para cada producto:
        demanda = (1/n) * Σ ventas[k]   con k desde 1 hasta n

    La sumatoria Σ se calcula con un ciclo for que va acumulando
    las ventas mes a mes.

    Parametros:
        historial_ventas: matriz con una fila por producto y una columna por mes.

    Retorna:
        Lista con la demanda promedio proyectada de cada producto.
    """
    demandas = []

    for ventas_producto in historial_ventas:
        n = len(ventas_producto)
        if n == 0:
            raise ValueError("El historial de ventas de un producto esta vacio (n = 0).")

        # Sumatoria: acumulamos las ventas de los n meses
        suma = 0
        for venta in ventas_producto:
            suma = suma + venta

        # Promedio = sumatoria dividida por n
        promedio = suma / n
        demandas.append(promedio)

    return demandas


def detectar_riesgo_quiebre(stock, demandas):
    """
    Detecta productos con riesgo de quiebre de stock.

    Para cada producto se suma su fila de stock (todas las sucursales):
        stock_total[i] = Σ S[i][j]
    Si stock_total[i] < demanda proyectada[i], hay riesgo de quiebre.

    Parametros:
        stock: matriz productos x sucursales.
        demandas: lista con la demanda proyectada de cada producto.

    Retorna:
        Lista de valores True/False (True = hay riesgo) en el orden de los productos.
    """
    matriz_stock = np.array(stock)

    # Debe haber una demanda por cada producto (fila)
    if matriz_stock.shape[0] != len(demandas):
        raise ValueError(
            f"Hay {matriz_stock.shape[0]} productos en el stock, pero "
            f"{len(demandas)} valores de demanda."
        )

    # Suma de cada fila (axis=1 significa "sumar a lo largo de las columnas")
    stock_total = matriz_stock.sum(axis=1)

    riesgos = []
    for i in range(len(demandas)):
        riesgos.append(bool(stock_total[i] < demandas[i]))
    return riesgos
