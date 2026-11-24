"""
main.py
-------
Programa principal de OptiMat.

Usa los datos de ejemplo de datos.py, aplica las funciones de calculos.py
e imprime un reporte en la consola.

Ejecutar con:  python main.py
"""

import numpy as np

from datos import PRODUCTOS, SUCURSALES, CAPACIDAD, STOCK, TARIFAS, HISTORIAL_VENTAS
from calculos import (
    calcular_reposicion,
    calcular_costos,
    proyectar_demanda,
    detectar_riesgo_quiebre,
)


def formato_pesos(valor):
    """Devuelve un numero con formato de pesos chilenos, por ejemplo $1.234.500."""
    texto = f"{valor:,.0f}"          # 1,234,500
    texto = texto.replace(",", ".")  # 1.234.500
    return "$" + texto


def imprimir_titulo(texto):
    """Imprime un titulo destacado."""
    print()
    print("=" * 60)
    print(texto)
    print("=" * 60)


def main():
    # 1. MATRICES: reposicion = capacidad - stock
    reposicion = calcular_reposicion(CAPACIDAD, STOCK)

    # 2. VECTORES: costo por producto y costo total
    costos, costo_total = calcular_costos(reposicion, TARIFAS)

    # 3. SUMATORIAS: demanda proyectada y riesgo de quiebre
    demandas = proyectar_demanda(HISTORIAL_VENTAS)
    riesgos = detectar_riesgo_quiebre(STOCK, demandas)
    stock_total = np.array(STOCK).sum(axis=1)

    # ---------------- Reporte ----------------
    print("OptiMat - Reporte de reposicion de inventario")

    imprimir_titulo("1) Unidades a despachar (Capacidad - Stock)")
    encabezado = f"{'Producto':<12}"
    for sucursal in SUCURSALES:
        encabezado += f"{sucursal:>10}"
    encabezado += f"{'Total':>10}"
    print(encabezado)
    print("-" * len(encabezado))
    for i, producto in enumerate(PRODUCTOS):
        fila = f"{producto:<12}"
        for j in range(len(SUCURSALES)):
            fila += f"{reposicion[i][j]:>10}"
        fila += f"{reposicion[i].sum():>10}"
        print(fila)

    imprimir_titulo("2) Costo de despacho (Reposicion x Tarifas)")
    print("Tarifa por unidad:", end=" ")
    print(", ".join(f"{SUCURSALES[j]} {formato_pesos(TARIFAS[j])}" for j in range(len(SUCURSALES))))
    print()
    for i, producto in enumerate(PRODUCTOS):
        print(f"{producto:<12}{formato_pesos(costos[i]):>15}")
    print("-" * 27)
    print(f"{'TOTAL':<12}{formato_pesos(costo_total):>15}")

    imprimir_titulo(f"3) Demanda proyectada (promedio de {len(HISTORIAL_VENTAS[0])} meses)")
    print(f"{'Producto':<12}{'Stock total':>12}{'Demanda':>10}  Estado")
    print("-" * 50)
    for i, producto in enumerate(PRODUCTOS):
        estado = "RIESGO DE QUIEBRE" if riesgos[i] else "OK"
        print(f"{producto:<12}{stock_total[i]:>12}{demandas[i]:>10.1f}  {estado}")

    imprimir_titulo("Alertas")
    hay_alertas = False
    for i, producto in enumerate(PRODUCTOS):
        if riesgos[i]:
            hay_alertas = True
            faltan = demandas[i] - stock_total[i]
            print(f"- {producto}: stock total {stock_total[i]} es menor que la demanda "
                  f"proyectada {demandas[i]:.1f} (faltan aprox. {faltan:.1f} unidades).")
    if not hay_alertas:
        print("No hay productos con riesgo de quiebre de stock.")


if __name__ == "__main__":
    main()
