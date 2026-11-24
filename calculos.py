"""
calculos.py
-----------
Funciones matematicas de OptiMat.

Todas las funciones son "puras": reciben datos, devuelven un resultado
y no imprimen nada ni modifican variables globales.
"""

import numpy as np


def calcular_reposicion(pedidos, entregado):
    """
    Calcula la matriz de despacho pendiente (RESTA DE MATRICES).

    Formula:  R = P - E
    donde P es la matriz de pedidos de los clientes y E la matriz de
    unidades ya entregadas. Cada elemento R[i][j] indica cuantas unidades
    del producto i faltan por enviar al cliente j.

    Parametros:
        pedidos: matriz (lista de listas o arreglo NumPy) productos x clientes.
        entregado: matriz con las mismas dimensiones que pedidos.

    Retorna:
        Arreglo NumPy con la matriz de despacho pendiente.
    """
    matriz_pedidos = np.array(pedidos)
    matriz_entregado = np.array(entregado)

    # Para restar dos matrices deben tener el mismo tamaño
    if matriz_pedidos.shape != matriz_entregado.shape:
        raise ValueError(
            f"Las matrices de pedidos {matriz_pedidos.shape} y de entregas "
            f"{matriz_entregado.shape} deben tener las mismas dimensiones."
        )

    # No se puede haber entregado mas de lo pedido (daria un despacho negativo)
    if np.any(matriz_entregado > matriz_pedidos):
        raise ValueError("Hay un cliente con mas unidades entregadas que pedidas.")

    # Resta elemento a elemento
    reposicion = matriz_pedidos - matriz_entregado
    return reposicion


def calcular_costos(reposicion, tarifas):
    """
    Calcula el costo de despacho (PRODUCTO MATRIZ x VECTOR).

    Formula:  costos = R * t
    donde R es la matriz de despacho pendiente (productos x clientes) y t es
    el vector de tarifas por unidad (una tarifa por cliente).
    Cada componente del resultado es:
        costos[i] = R[i][0]*t[0] + R[i][1]*t[1] + ... (costo del producto i)

    El costo logistico total es la suma de todas las componentes del vector.

    Parametros:
        reposicion: matriz productos x clientes.
        tarifas: vector con una tarifa por cliente (columna).

    Retorna:
        Una tupla (vector_costos, costo_total).
    """
    matriz_reposicion = np.array(reposicion)
    vector_tarifas = np.array(tarifas)

    # La cantidad de columnas de la matriz debe ser igual al largo del vector
    if matriz_reposicion.shape[1] != vector_tarifas.shape[0]:
        raise ValueError(
            f"La matriz de despacho tiene {matriz_reposicion.shape[1]} clientes "
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


def verificar_despacho(stock_bodega, reposicion):
    """
    Revisa si el stock de la bodega alcanza para despachar lo pendiente
    (SUMATORIA POR FILA).

    Para cada producto se suma su fila de la matriz de despacho (todos los
    clientes):
        total_pendiente[i] = Σ R[i][j]
    Si stock_bodega[i] < total_pendiente[i], no alcanza para cumplir todos
    los pedidos de ese producto.

    Parametros:
        stock_bodega: vector con las unidades disponibles de cada producto.
        reposicion: matriz de despacho pendiente productos x clientes.

    Retorna:
        Tupla (total_pendiente, faltantes): el total por despachar de cada
        producto y cuantas unidades faltan en bodega (0 si alcanza).
    """
    vector_bodega = np.array(stock_bodega)
    matriz_reposicion = np.array(reposicion)

    # Debe haber un valor de bodega por cada producto (fila)
    if matriz_reposicion.shape[0] != vector_bodega.shape[0]:
        raise ValueError(
            f"Hay {matriz_reposicion.shape[0]} productos en la matriz de despacho, "
            f"pero {vector_bodega.shape[0]} valores de stock en bodega."
        )

    # Suma de cada fila (axis=1 significa "sumar a lo largo de las columnas")
    total_pendiente = matriz_reposicion.sum(axis=1)

    # Si la bodega tiene menos de lo pendiente, la diferencia es lo que falta
    faltantes = np.maximum(total_pendiente - vector_bodega, 0)
    return total_pendiente, faltantes


def detectar_riesgo_quiebre(stock_bodega, demandas):
    """
    Detecta productos con riesgo de quiebre de stock.

    Compara el stock de la bodega de cada producto con su demanda
    proyectada: si stock_bodega[i] < demanda[i], hay riesgo de quiebre.

    Parametros:
        stock_bodega: vector con las unidades disponibles de cada producto.
        demandas: lista con la demanda proyectada de cada producto.

    Retorna:
        Lista de valores True/False (True = hay riesgo) en el orden de los productos.
    """
    vector_bodega = np.array(stock_bodega)

    # Debe haber una demanda por cada producto
    if vector_bodega.shape[0] != len(demandas):
        raise ValueError(
            f"Hay {vector_bodega.shape[0]} productos en bodega, pero "
            f"{len(demandas)} valores de demanda."
        )

    riesgos = []
    for i in range(len(demandas)):
        riesgos.append(bool(vector_bodega[i] < demandas[i]))
    return riesgos


def resumir_ventas(ventas):
    """
    Resume el arreglo de ventas de 3 dimensiones (ARREGLO MULTIDIMENSIONAL
    y SUMATORIA POR EJE).

    ventas[i][j][k] = unidades del producto i vendidas al cliente j en el mes k.
    Sumar sobre un eje elimina esa dimension:
        ventas_por_mes[i][k]     = Σ_j ventas[i][j][k]   (se suman los clientes)
        ventas_por_cliente[i][j] = Σ_k ventas[i][j][k]   (se suman los meses)

    Parametros:
        ventas: arreglo productos x clientes x meses.

    Retorna:
        Tupla (ventas_por_mes, ventas_por_cliente):
        matriz productos x meses y matriz productos x clientes.
    """
    arreglo_ventas = np.array(ventas)

    # Debe tener exactamente 3 indices: producto, cliente y mes
    if arreglo_ventas.ndim != 3:
        raise ValueError(
            f"Las ventas deben tener 3 dimensiones (producto, cliente, mes), "
            f"pero tienen {arreglo_ventas.ndim}."
        )
    if arreglo_ventas.size == 0:
        raise ValueError("El arreglo de ventas esta vacio.")

    # axis=1 es el eje de los clientes; axis=2 es el eje de los meses
    ventas_por_mes = arreglo_ventas.sum(axis=1)
    ventas_por_cliente = arreglo_ventas.sum(axis=2)
    return ventas_por_mes, ventas_por_cliente


def calcular_cobertura(stock_bodega, demandas, dias_por_mes=30):
    """
    Calcula los dias de cobertura de cada producto: cuantos dias alcanza el
    stock de la bodega al ritmo de venta actual (DIVISION / PROPORCION).

    Formula para cada producto:
        venta_diaria = demanda_mensual / dias_por_mes
        cobertura    = stock_bodega / venta_diaria

    Si un producto no tiene demanda, su stock nunca se agota (cobertura infinita).

    Parametros:
        stock_bodega: vector con las unidades disponibles de cada producto.
        demandas: lista con la demanda mensual proyectada de cada producto.
        dias_por_mes: cantidad de dias que se consideran en un mes.

    Retorna:
        Lista con los dias de cobertura de cada producto.
    """
    if len(stock_bodega) != len(demandas):
        raise ValueError(
            f"Hay {len(stock_bodega)} productos en bodega, pero "
            f"{len(demandas)} valores de demanda."
        )

    coberturas = []
    for i in range(len(demandas)):
        if demandas[i] <= 0:
            coberturas.append(float("inf"))
        else:
            venta_diaria = demandas[i] / dias_por_mes
            coberturas.append(stock_bodega[i] / venta_diaria)
    return coberturas


def clasificar_alertas(coberturas, umbral_verde=30, umbral_amarillo=20):
    """
    Clasifica cada producto en un semaforo segun sus dias de cobertura
    (DESIGUALDADES):

        VERDE    si cobertura >= umbral_verde
        AMARILLO si umbral_amarillo <= cobertura < umbral_verde
        ROJO     si cobertura < umbral_amarillo

    Parametros:
        coberturas: lista con los dias de cobertura de cada producto.
        umbral_verde: dias desde los que el stock se considera suficiente.
        umbral_amarillo: dias bajo los que el stock es critico.

    Retorna:
        Lista con "VERDE", "AMARILLO" o "ROJO" para cada producto.
    """
    if umbral_amarillo >= umbral_verde:
        raise ValueError("El umbral amarillo debe ser menor que el umbral verde.")

    alertas = []
    for dias in coberturas:
        if dias >= umbral_verde:
            alertas.append("VERDE")
        elif dias >= umbral_amarillo:
            alertas.append("AMARILLO")
        else:
            alertas.append("ROJO")
    return alertas
