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

# HISTORIAL DE VENTAS de los ultimos 6 meses (unidades vendidas en total,
# sumando todos los clientes). Una fila por producto, una columna por mes.
#           mes1 mes2 mes3 mes4 mes5 mes6
HISTORIAL_VENTAS = [
    [80, 95, 90, 85, 100, 92],    # Teclados
    [25, 30, 28, 32, 27, 30],     # Monitores
    [120, 130, 125, 140, 135, 128],  # Mouse
    [15, 18, 20, 16, 19, 22],     # Notebooks
]
