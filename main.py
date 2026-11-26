"""
main.py
-------
Programa principal de OptiMat (version interactiva).

Muestra un MENU en la consola para que el usuario pueda:
    - ver el reporte completo de despachos, costos y alertas,
    - registrar pedidos nuevos y entregas a los clientes,
    - recibir mercaderia del proveedor (aumentar el stock),
    - registrar las ventas de un mes nuevo,
    - cambiar las tarifas de flete y los umbrales del semaforo.

Cada cambio vuelve a pasar por las funciones matematicas de calculos.py,
asi que el reporte siempre refleja los datos actuales. Los cambios se
guardan en optimat_datos.json para no perderlos al cerrar el programa.

Ejecutar con:
    python main.py            -> menu interactivo
    python main.py --reporte  -> solo imprime el reporte (sin menu)
"""

import copy
import json
import os
import sys

import datos
from calculos import (
    calcular_reposicion,
    calcular_costos,
    verificar_despacho,
    proyectar_demanda,
    detectar_riesgo_quiebre,
    resumir_ventas,
    calcular_cumplimiento,
    clasificar_alertas,
    calcular_pedido_sugerido,
)
from graficos import graficar_alertas

# Carpeta donde esta este archivo: ahi se guardan los datos y el grafico
CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(CARPETA, "optimat_datos.json")
ARCHIVO_GRAFICO = os.path.join(CARPETA, "alertas.png")


# ======================================================================
# Datos del programa (estado)
# ======================================================================

def datos_de_ejemplo():
    """Devuelve una copia de los datos de ejemplo de datos.py."""
    return copy.deepcopy({
        "productos": datos.PRODUCTOS,
        "clientes": datos.CLIENTES,
        "clientes_corto": datos.CLIENTES_CORTO,
        "pedidos": datos.PEDIDOS,
        "entregado": datos.ENTREGADO,
        "tarifas": datos.TARIFAS,
        "stock": datos.STOCK_BODEGA,
        "ventas": datos.VENTAS,
        "umbral_verde": datos.UMBRAL_VERDE,
        "umbral_amarillo": datos.UMBRAL_AMARILLO,
        "unidad_umbral": "porcentaje",
    })


def cargar_datos():
    """Carga los datos guardados; si no hay, usa los datos de ejemplo."""
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, encoding="utf-8") as archivo:
                estado = json.load(archivo)
            print(f"Datos cargados desde {os.path.basename(ARCHIVO_DATOS)}.")
            # Archivos de versiones anteriores tenian los umbrales en dias
            if estado.get("unidad_umbral") != "porcentaje":
                estado["umbral_verde"] = datos.UMBRAL_VERDE
                estado["umbral_amarillo"] = datos.UMBRAL_AMARILLO
                estado["unidad_umbral"] = "porcentaje"
            return estado
        except (OSError, json.JSONDecodeError):
            print("No se pudo leer el archivo de datos; se usan los datos de ejemplo.")
    return datos_de_ejemplo()


def guardar_datos(estado):
    """Guarda los datos actuales en un archivo JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(estado, archivo, ensure_ascii=False, indent=2)


def calcular_todo(estado):
    """Aplica todas las funciones matematicas y devuelve los resultados."""
    reposicion = calcular_reposicion(estado["pedidos"], estado["entregado"])
    costos, costo_total = calcular_costos(reposicion, estado["tarifas"])
    total_pendiente, faltantes = verificar_despacho(estado["stock"], reposicion)
    ventas_por_mes, ventas_por_cliente = resumir_ventas(estado["ventas"])
    demandas = proyectar_demanda(ventas_por_mes)
    riesgos = detectar_riesgo_quiebre(estado["stock"], demandas)
    cumplimientos = calcular_cumplimiento(estado["stock"], total_pendiente)
    niveles = clasificar_alertas(cumplimientos, estado["umbral_verde"], estado["umbral_amarillo"])
    sugeridos = calcular_pedido_sugerido(estado["stock"], total_pendiente, demandas)
    return {
        "reposicion": reposicion, "costos": costos, "costo_total": costo_total,
        "total_pendiente": total_pendiente, "faltantes": faltantes,
        "ventas_por_cliente": ventas_por_cliente, "demandas": demandas,
        "riesgos": riesgos, "cumplimientos": cumplimientos, "niveles": niveles,
        "sugeridos": sugeridos,
    }


# ======================================================================
# Formato e impresion
# ======================================================================

def formato_pesos(valor):
    """Devuelve un numero con formato de pesos chilenos, por ejemplo $1.234.500."""
    texto = f"{valor:,.0f}"          # 1,234,500
    texto = texto.replace(",", ".")  # 1.234.500
    return "$" + texto


def formato_porcentaje(valor):
    """Devuelve un porcentaje sin decimales, o 'sin pend.' si no hay pendientes."""
    if valor == float("inf"):
        return "sin pend."
    return f"{valor:.0f} %"


def imprimir_titulo(texto):
    """Imprime un titulo destacado."""
    print()
    print("=" * 60)
    print(texto)
    print("=" * 60)


def imprimir_matriz(estado, matriz, total_por_fila=True):
    """Imprime una matriz productos x clientes con encabezados."""
    encabezado = f"{'Producto':<12}"
    for cliente in estado["clientes_corto"]:
        encabezado += f"{cliente:>11}"
    if total_por_fila:
        encabezado += f"{'Total':>9}"
    print(encabezado)
    print("-" * len(encabezado))
    for i, producto in enumerate(estado["productos"]):
        fila = f"{producto:<12}"
        for valor in matriz[i]:
            fila += f"{int(valor):>11}"
        if total_por_fila:
            fila += f"{int(sum(matriz[i])):>9}"
        print(fila)


def imprimir_reporte(estado):
    """Imprime el reporte completo con los datos actuales."""
    r = calcular_todo(estado)
    productos = estado["productos"]
    stock = estado["stock"]
    verde, amarillo = estado["umbral_verde"], estado["umbral_amarillo"]

    print()
    print("OptiMat - Reporte de despachos a clientes")
    print("Clientes: " + ", ".join(estado["clientes"]))

    imprimir_titulo("1) Unidades por despachar (Pedidos - Entregado)")
    imprimir_matriz(estado, r["reposicion"])

    imprimir_titulo("2) Costo de despacho (Despacho x Tarifas)")
    print("Tarifa por unidad: " + ", ".join(
        f"{c} {formato_pesos(t)}" for c, t in zip(estado["clientes_corto"], estado["tarifas"])))
    print()
    for i, producto in enumerate(productos):
        print(f"{producto:<12}{formato_pesos(r['costos'][i]):>15}")
    print("-" * 27)
    print(f"{'TOTAL':<12}{formato_pesos(r['costo_total']):>15}")

    imprimir_titulo("3) Bodega vs. despachos pendientes")
    print(f"{'Producto':<12}{'Bodega':>8}{'Pendiente':>11}  Estado")
    print("-" * 50)
    for i, producto in enumerate(productos):
        estado_txt = f"FALTAN {r['faltantes'][i]}" if r["faltantes"][i] > 0 else "ALCANZA"
        print(f"{producto:<12}{stock[i]:>8}{r['total_pendiente'][i]:>11}  {estado_txt}")

    n_meses = len(estado["ventas"][0][0])
    imprimir_titulo(f"4) Demanda proyectada (promedio de {n_meses} meses)")
    print(f"{'Producto':<12}{'Bodega':>8}{'Demanda':>10}  Estado")
    print("-" * 50)
    for i, producto in enumerate(productos):
        estado_txt = "RIESGO DE QUIEBRE" if r["riesgos"][i] else "OK"
        print(f"{producto:<12}{stock[i]:>8}{r['demandas'][i]:>10.1f}  {estado_txt}")

    imprimir_titulo(f"5) Ventas por cliente (suma de los {n_meses} meses)")
    imprimir_matriz(estado, r["ventas_por_cliente"])

    imprimir_titulo("6) Semaforo de stock (Bodega / Pendiente x 100)")
    print(f"Verde: {verde} % o mas | Amarillo: {amarillo} % a {verde} %"
          f" | Rojo: menos de {amarillo} % (no alcanza)")
    print()
    print(f"{'Producto':<12}{'Bodega':>8}{'Pendiente':>11}{'Cumplim.':>10}  Alerta")
    print("-" * 52)
    for i, producto in enumerate(productos):
        print(f"{producto:<12}{stock[i]:>8}{r['total_pendiente'][i]:>11}"
              f"{formato_porcentaje(r['cumplimientos'][i]):>10}  {r['niveles'][i]}")

    imprimir_titulo("7) Pedido sugerido al proveedor (Pendiente + Demanda - Bodega)")
    print(f"{'Producto':<12}{'Bodega':>8}{'Pendiente':>11}{'Demanda':>10}{'Comprar':>10}")
    print("-" * 51)
    for i, producto in enumerate(productos):
        print(f"{producto:<12}{stock[i]:>8}{r['total_pendiente'][i]:>11}"
              f"{r['demandas'][i]:>10.1f}{r['sugeridos'][i]:>10}")

    imprimir_titulo("Alertas")
    hay_alertas = False
    for i, producto in enumerate(productos):
        if r["faltantes"][i] > 0:
            hay_alertas = True
            print(f"- {producto}: faltan {r['faltantes'][i]} unidades en bodega para cumplir "
                  f"los pedidos pendientes ({r['total_pendiente'][i]}).")
        if r["riesgos"][i]:
            hay_alertas = True
            print(f"- {producto}: stock en bodega {stock[i]} es menor que la demanda "
                  f"proyectada {r['demandas'][i]:.1f}. Conviene reponer pronto.")
    if not hay_alertas:
        print("No hay alertas.")


def resumen_rapido(estado):
    """Imprime un resumen corto despues de cada cambio."""
    r = calcular_todo(estado)
    print()
    print(f"  Costo total de despacho pendiente: {formato_pesos(r['costo_total'])}")
    for i, producto in enumerate(estado["productos"]):
        extra = f", faltan {r['faltantes'][i]}" if r["faltantes"][i] > 0 else ""
        print(f"  {producto:<11} bodega {estado['stock'][i]:>4} | pendiente "
              f"{r['total_pendiente'][i]:>4} | {formato_porcentaje(r['cumplimientos'][i]):>6} "
              f"-> {r['niveles'][i]}{extra}")


# ======================================================================
# Lectura de datos por teclado
# ======================================================================

def leer_entero(mensaje, minimo=None, maximo=None):
    """Pide un numero entero hasta que el usuario escriba uno valido."""
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("  Debe escribir un numero entero.")
            continue
        if minimo is not None and valor < minimo:
            print(f"  El valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"  El valor debe ser menor o igual a {maximo}.")
        else:
            return valor


def elegir(titulo, opciones):
    """Muestra una lista numerada y devuelve el indice (desde 0) elegido."""
    print(titulo)
    for k, opcion in enumerate(opciones, start=1):
        print(f"  {k}. {opcion}")
    return leer_entero("Opcion: ", 1, len(opciones)) - 1


def confirmar(mensaje):
    """Devuelve True si el usuario responde s (si)."""
    return input(mensaje + " (s/n): ").strip().lower() in ("s", "si", "sí")


# ======================================================================
# Acciones del menu
# ======================================================================

def registrar_pedido(estado):
    """Un cliente pide mas unidades: P[i][j] = P[i][j] + cantidad."""
    i = elegir("Producto:", estado["productos"])
    j = elegir("Cliente:", estado["clientes"])
    cantidad = leer_entero("Unidades pedidas: ", 1)
    estado["pedidos"][i][j] += cantidad
    print(f"\nPedido registrado: {cantidad} {estado['productos'][i]} para "
          f"{estado['clientes'][j]}.")
    return True


def registrar_entrega(estado):
    """
    Se despachan unidades a un cliente:
    E[i][j] = E[i][j] + cantidad   y   bodega[i] = bodega[i] - cantidad.
    """
    reposicion = calcular_reposicion(estado["pedidos"], estado["entregado"])
    i = elegir("Producto:", estado["productos"])
    j = elegir("Cliente:", estado["clientes"])
    pendiente = int(reposicion[i][j])
    maximo = min(pendiente, estado["stock"][i])
    print(f"Pendiente para este cliente: {pendiente} | En bodega: {estado['stock'][i]}")
    if maximo == 0:
        print("No se puede entregar: no hay unidades pendientes o no hay stock.")
        return False
    cantidad = leer_entero(f"Unidades entregadas (1 a {maximo}): ", 1, maximo)
    estado["entregado"][i][j] += cantidad
    estado["stock"][i] -= cantidad
    print(f"\nEntrega registrada: {cantidad} {estado['productos'][i]} a "
          f"{estado['clientes'][j]}. Costo de este flete: "
          f"{formato_pesos(cantidad * estado['tarifas'][j])}.")
    return True


def recibir_mercaderia(estado):
    """Llega mercaderia del proveedor: bodega[i] = bodega[i] + cantidad."""
    r = calcular_todo(estado)
    print("Pedido sugerido por OptiMat: " + ", ".join(
        f"{p} {s}" for p, s in zip(estado["productos"], r["sugeridos"])))
    i = elegir("Producto recibido:", estado["productos"])
    cantidad = leer_entero("Unidades recibidas: ", 1)
    estado["stock"][i] += cantidad
    print(f"\nStock de {estado['productos'][i]} actualizado a {estado['stock'][i]} unidades.")
    return True


def registrar_ventas_mes(estado):
    """
    Agrega un mes nuevo de ventas a cada producto y cliente. Se mantiene una
    ventana de los ultimos meses: el mes mas antiguo se descarta, asi el
    promedio (la demanda proyectada) se va actualizando (promedio movil).
    """
    clientes = estado["clientes_corto"]
    print("Escriba las unidades vendidas a cada cliente en el mes, separadas por espacio.")
    print("Orden de los clientes: " + ", ".join(clientes))
    nuevas = []
    for producto in estado["productos"]:
        while True:
            texto = input(f"  {producto}: ").split()
            try:
                valores = [int(v) for v in texto]
            except ValueError:
                print("  Solo numeros enteros, por favor.")
                continue
            if len(valores) != len(clientes) or any(v < 0 for v in valores):
                print(f"  Debe escribir {len(clientes)} numeros mayores o iguales a 0.")
                continue
            nuevas.append(valores)
            break

    for i, valores in enumerate(nuevas):
        for j, venta in enumerate(valores):
            serie = estado["ventas"][i][j]
            serie.append(venta)  # el mes nuevo entra al final
            serie.pop(0)         # el mes mas antiguo sale
    print("\nVentas registradas. La demanda proyectada usa ahora los ultimos "
          f"{len(estado['ventas'][0][0])} meses.")
    return True


def cambiar_tarifas(estado):
    """Modifica el vector de tarifas de flete por cliente."""
    print("Tarifas actuales: " + ", ".join(
        f"{c} {formato_pesos(t)}" for c, t in zip(estado["clientes_corto"], estado["tarifas"])))
    j = elegir("Cliente a modificar:", estado["clientes"])
    estado["tarifas"][j] = leer_entero("Nueva tarifa por unidad (CLP): ", 0)
    print(f"\nTarifa de {estado['clientes'][j]} actualizada a "
          f"{formato_pesos(estado['tarifas'][j])}.")
    return True


def cambiar_umbrales(estado):
    """Modifica los porcentajes de cumplimiento que definen el semaforo."""
    print(f"Actuales: verde desde {estado['umbral_verde']} %, "
          f"amarillo desde {estado['umbral_amarillo']} %.")
    verde = leer_entero("Nuevo umbral verde (%): ", 2)
    amarillo = leer_entero(f"Nuevo umbral amarillo (%, menor que {verde}): ", 1, verde - 1)
    estado["umbral_verde"], estado["umbral_amarillo"] = verde, amarillo
    print("\nUmbrales actualizados.")
    return True


def generar_grafico(estado):
    """Genera el grafico del semaforo y lo intenta abrir."""
    r = calcular_todo(estado)
    archivo = graficar_alertas(estado["productos"], r["cumplimientos"], r["niveles"],
                               estado["umbral_verde"], estado["umbral_amarillo"],
                               archivo=ARCHIVO_GRAFICO)
    print(f"Grafico guardado en {archivo}")
    if hasattr(os, "startfile"):  # solo existe en Windows
        try:
            os.startfile(archivo)
        except OSError:
            pass
    return False


def restaurar_ejemplo(estado):
    """Vuelve a los datos de ejemplo de datos.py."""
    if not confirmar("Se perderan los cambios. ¿Restaurar los datos de ejemplo?"):
        return False
    estado.clear()
    estado.update(datos_de_ejemplo())
    print("\nDatos de ejemplo restaurados.")
    return True


# ======================================================================
# Menu principal
# ======================================================================

OPCIONES = [
    ("Ver reporte completo", None),
    ("Registrar un pedido nuevo de un cliente", registrar_pedido),
    ("Registrar una entrega a un cliente", registrar_entrega),
    ("Recibir mercaderia del proveedor (aumentar stock)", recibir_mercaderia),
    ("Registrar las ventas de un mes nuevo", registrar_ventas_mes),
    ("Cambiar tarifas de flete", cambiar_tarifas),
    ("Cambiar umbrales del semaforo", cambiar_umbrales),
    ("Generar grafico del semaforo", generar_grafico),
    ("Restaurar datos de ejemplo", restaurar_ejemplo),
]


def menu(estado):
    """Ciclo del menu: se repite hasta que el usuario elige salir."""
    while True:
        imprimir_titulo("OptiMat - Menu principal")
        for k, (texto, _) in enumerate(OPCIONES, start=1):
            print(f"  {k}. {texto}")
        print("  0. Salir")
        opcion = leer_entero("Elija una opcion: ", 0, len(OPCIONES))

        if opcion == 0:
            print("Datos guardados. ¡Hasta luego!")
            return
        texto, accion = OPCIONES[opcion - 1]
        imprimir_titulo(texto)
        if accion is None:
            imprimir_reporte(estado)
        elif accion(estado):
            # Hubo un cambio: se guarda y se muestra como quedo todo
            guardar_datos(estado)
            resumen_rapido(estado)
        input("\nPresione Enter para volver al menu...")


def main():
    estado = cargar_datos()
    if "--reporte" in sys.argv:
        imprimir_reporte(estado)
        return
    try:
        menu(estado)
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma cerrado.")


if __name__ == "__main__":
    main()
