"""
datos.py
--------
Datos de ejemplo de OptiMat.

Representan el inventario de una pyme de retail tecnologico con tres
sucursales. Son valores inventados, pero realistas, para probar el programa.

Convencion de las matrices:
    - cada FILA es un producto   (en el orden de la lista PRODUCTOS)
    - cada COLUMNA es una sucursal (en el orden de la lista SUCURSALES)
"""

# Nombres de los productos (filas de las matrices)
PRODUCTOS = ["Teclados", "Monitores", "Mouse", "Notebooks"]

# Nombres de las sucursales (columnas de las matrices)
SUCURSALES = ["Norte", "Centro", "Sur"]

# Matriz de CAPACIDAD MAXIMA: cuantas unidades caben en cada sucursal.
#                Norte  Centro  Sur
CAPACIDAD = [
    [120, 150, 100],  # Teclados
    [60, 80, 50],     # Monitores
    [200, 250, 180],  # Mouse
    [40, 50, 30],     # Notebooks
]

# Matriz de STOCK ACTUAL: cuantas unidades hay hoy en cada sucursal.
# Cada valor es menor o igual que su capacidad.
#                Norte  Centro  Sur
STOCK = [
    [85, 110, 40],    # Teclados
    [20, 55, 35],     # Monitores
    [150, 90, 160],   # Mouse
    [12, 30, 8],      # Notebooks
]

# Vector de TARIFAS de flete: costo (en pesos chilenos, CLP) de enviar
# UNA unidad desde la bodega central a cada sucursal.
#           Norte  Centro  Sur
TARIFAS = [3500, 2000, 4500]

# HISTORIAL DE VENTAS de los ultimos 6 meses (unidades vendidas en total,
# sumando todas las sucursales). Una fila por producto, una columna por mes.
#           mes1 mes2 mes3 mes4 mes5 mes6
HISTORIAL_VENTAS = [
    [180, 200, 190, 210, 220, 200],  # Teclados
    [95, 110, 120, 105, 115, 125],   # Monitores
    [300, 320, 310, 290, 330, 350],  # Mouse
    [45, 50, 55, 60, 52, 58],        # Notebooks
]
