"""
main.py
-------
Programa principal de OptiMat.

Usa los datos de ejemplo de datos.py, aplica las funciones de calculos.py
e imprime un reporte en la consola.

Ejecutar con:  python main.py
"""

from datos import (
    PRODUCTOS, CLIENTES, CLIENTES_CORTO, PEDIDOS, ENTREGADO,
    TARIFAS, STOCK_BODEGA, HISTORIAL_VENTAS,
)
from calculos import (
    calcular_reposicion,
    calcular_costos,
    verificar_despacho,
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
    # 1. MATRICES: despacho pendiente = pedidos - entregado
    reposicion = calcular_reposicion(PEDIDOS, ENTREGADO)

    # 2. VECTORES: costo por producto y costo total
    costos, costo_total = calcular_costos(reposicion, TARIFAS)

    # 3. SUMATORIAS: total pendiente por producto, demanda proyectada y riesgo
    total_pendiente, faltantes = verificar_despacho(STOCK_BODEGA, reposicion)
    demandas = proyectar_demanda(HISTORIAL_VENTAS)
    riesgos = detectar_riesgo_quiebre(STOCK_BODEGA, demandas)

    # ---------------- Reporte ----------------
    print("OptiMat - Reporte de despachos a clientes")
    print("Clientes: " + ", ".join(CLIENTES))

    imprimir_titulo("1) Unidades por despachar (Pedidos - Entregado)")
    encabezado = f"{'Producto':<12}"
    for cliente in CLIENTES_CORTO:
        encabezado += f"{cliente:>11}"
    encabezado += f"{'Total':>9}"
    print(encabezado)
    print("-" * len(encabezado))
    for i, producto in enumerate(PRODUCTOS):
        fila = f"{producto:<12}"
        for j in range(len(CLIENTES)):
            fila += f"{reposicion[i][j]:>11}"
        fila += f"{total_pendiente[i]:>9}"
        print(fila)

    imprimir_titulo("2) Costo de despacho (Despacho x Tarifas)")
    print("Tarifa por unidad:", end=" ")
    print(", ".join(f"{CLIENTES_CORTO[j]} {formato_pesos(TARIFAS[j])}" for j in range(len(CLIENTES))))
    print()
    for i, producto in enumerate(PRODUCTOS):
        print(f"{producto:<12}{formato_pesos(costos[i]):>15}")
    print("-" * 27)
    print(f"{'TOTAL':<12}{formato_pesos(costo_total):>15}")

    imprimir_titulo("3) Bodega vs. despachos pendientes")
    print(f"{'Producto':<12}{'Bodega':>8}{'Pendiente':>11}  Estado")
    print("-" * 50)
    for i, producto in enumerate(PRODUCTOS):
        estado = f"FALTAN {faltantes[i]}" if faltantes[i] > 0 else "ALCANZA"
        print(f"{producto:<12}{STOCK_BODEGA[i]:>8}{total_pendiente[i]:>11}  {estado}")

    imprimir_titulo(f"4) Demanda proyectada (promedio de {len(HISTORIAL_VENTAS[0])} meses)")
    print(f"{'Producto':<12}{'Bodega':>8}{'Demanda':>10}  Estado")
    print("-" * 50)
    for i, producto in enumerate(PRODUCTOS):
        estado = "RIESGO DE QUIEBRE" if riesgos[i] else "OK"
        print(f"{producto:<12}{STOCK_BODEGA[i]:>8}{demandas[i]:>10.1f}  {estado}")

    imprimir_titulo("Alertas")
    hay_alertas = False
    for i, producto in enumerate(PRODUCTOS):
        if faltantes[i] > 0:
            hay_alertas = True
            print(f"- {producto}: faltan {faltantes[i]} unidades en bodega para cumplir "
                  f"los pedidos pendientes ({total_pendiente[i]}).")
        if riesgos[i]:
            hay_alertas = True
            print(f"- {producto}: stock en bodega {STOCK_BODEGA[i]} es menor que la demanda "
                  f"proyectada {demandas[i]:.1f}. Conviene reponer pronto.")
    if not hay_alertas:
        print("No hay alertas.")


if __name__ == "__main__":
    main()
