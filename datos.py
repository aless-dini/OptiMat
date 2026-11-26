"""
datos.py
--------
Datos de ejemplo de OptiMat.

Representan a una pyme de retail tecnologico que tiene UNA bodega y vende
a varios clientes (por ejemplo, colegios u oficinas). Son valores
inventados, pero realistas, para probar el programa.

Convencion de las matrices:
    - cada FILA es un producto   (en el orden de la lista PRODUCTOS)
    - cada COLUMNA es un cliente (en el orden de la lista CLIENTES)
"""

# Nombres de los productos (filas de las matrices)
PRODUCTOS = ["Teclados", "Monitores", "Mouse", "Notebooks"]

# Nombres de los clientes (columnas de las matrices)
CLIENTES = ["Cliente A (La Serena)", "Cliente B (Coquimbo)", "Cliente C (Ovalle)"]

# Nombres cortos para que el reporte quepa en la consola
CLIENTES_CORTO = ["Cliente A", "Cliente B", "Cliente C"]

# Matriz de PEDIDOS: cuantas unidades de cada producto pidio cada cliente.
#              Cli. A  Cli. B  Cli. C
PEDIDOS = [
    [40, 25, 30],   # Teclados
    [15, 10, 12],   # Monitores
    [60, 35, 40],   # Mouse
    [10, 6, 8],     # Notebooks
]

# Matriz de ENTREGADO: cuantas unidades ya se le entregaron a cada cliente.
# Cada valor es menor o igual que lo pedido.
#              Cli. A  Cli. B  Cli. C
ENTREGADO = [
    [20, 25, 10],   # Teclados
    [5, 4, 12],     # Monitores
    [30, 15, 0],    # Mouse
    [4, 6, 2],      # Notebooks
]

# Vector de TARIFAS de flete: costo (en pesos chilenos, CLP) de enviar
# UNA unidad desde la bodega de la pyme a cada cliente.
#           Cli. A  Cli. B  Cli. C
TARIFAS = [1500, 2500, 4000]

# Vector de STOCK EN BODEGA: unidades disponibles hoy de cada producto.
#               Teclados  Monitores  Mouse  Notebooks
STOCK_BODEGA = [110, 35, 125, 9]

# VENTAS de los ultimos 6 meses: ARREGLO MULTIDIMENSIONAL de 3 indices.
#     VENTAS[i][j][k] = unidades del producto i vendidas al cliente j en el mes k
# Dimensiones: 4 productos x 3 clientes x 6 meses (72 datos).
# Se puede ver como 4 matrices (una por producto) de 3 clientes x 6 meses.
#                 mes1 mes2 mes3 mes4 mes5 mes6
VENTAS = [
    [   # Teclados
        [35, 44, 40, 39, 44, 42],   # Cliente A
        [23, 28, 27, 24, 30, 28],   # Cliente B
        [22, 23, 23, 22, 26, 22],   # Cliente C
    ],
    [   # Monitores
        [9, 13, 10, 14, 10, 13],
        [7, 10, 9, 10, 9, 10],
        [9, 7, 9, 8, 8, 7],
    ],
    [   # Mouse
        [49, 56, 52, 60, 56, 55],
        [35, 39, 38, 41, 40, 38],
        [36, 35, 35, 39, 39, 35],
    ],
    [   # Notebooks
        [6, 9, 8, 8, 8, 11],
        [3, 4, 5, 3, 5, 6],
        [6, 5, 7, 5, 6, 5],
    ],
]

# UMBRALES del semaforo de stock, en PORCENTAJE DE CUMPLIMIENTO
# (stock en bodega dividido por lo pendiente de despachar, por 100).
#   verde: 150 % o mas | amarillo: desde 100 % hasta menos de 150 % | rojo: menos de 100 %
UMBRAL_VERDE = 150
UMBRAL_AMARILLO = 100
