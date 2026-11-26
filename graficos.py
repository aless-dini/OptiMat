"""
graficos.py
-----------
Graficos de OptiMat hechos con Matplotlib.

El grafico se guarda como imagen (PNG), asi funciona igual en cualquier
computador, aunque no tenga pantalla.
"""

import matplotlib

matplotlib.use("Agg")  # dibuja en un archivo, sin abrir ventanas
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Colores del semaforo
COLORES = {"VERDE": "#2E9E5B", "AMARILLO": "#E3B505", "ROJO": "#D64545"}


def graficar_alertas(productos, cumplimientos, alertas, umbral_verde=150,
                     umbral_amarillo=100, archivo="alertas.png"):
    """
    Dibuja un grafico de barras con el porcentaje de cumplimiento de cada
    producto (stock en bodega / pendiente por despachar x 100), pintando cada
    barra con el color de su alerta y marcando los umbrales.

    Parametros:
        productos: nombres de los productos (eje horizontal).
        cumplimientos: porcentaje de cumplimiento de cada producto (alto de cada barra).
        alertas: "VERDE", "AMARILLO" o "ROJO" para cada producto.
        umbral_verde, umbral_amarillo: lineas de referencia en porcentaje.
        archivo: ruta del PNG que se genera.

    Retorna:
        La ruta del archivo generado.
    """
    if not (len(productos) == len(cumplimientos) == len(alertas)):
        raise ValueError("Productos, cumplimientos y alertas deben tener el mismo largo.")

    # Un producto sin pedidos pendientes (infinito) se dibuja con un tope visible
    finitos = [c for c in cumplimientos if c != float("inf")]
    tope = max(finitos + [umbral_verde]) * 1.25
    alturas = [min(c, tope) for c in cumplimientos]
    colores = [COLORES[a] for a in alertas]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.bar(productos, alturas, color=colores, width=0.6)

    # Lineas de los umbrales
    ax.axhline(umbral_verde, color=COLORES["VERDE"], linestyle="--", linewidth=1, zorder=0)
    ax.axhline(umbral_amarillo, color=COLORES["ROJO"], linestyle="--", linewidth=1, zorder=0)

    # Porcentaje sobre cada barra
    for barra, porcentaje in zip(barras, cumplimientos):
        if porcentaje == float("inf"):
            texto = "sin pendientes"
        else:
            texto = f"{porcentaje:.0f} %"
        ax.annotate(texto, (barra.get_x() + barra.get_width() / 2, barra.get_height()),
                    ha="center", va="bottom", xytext=(0, 4), textcoords="offset points",
                    bbox=dict(facecolor="white", edgecolor="none", pad=1))

    ax.set_title("Semáforo de stock: stock en bodega respecto a lo pendiente por despachar")
    ax.set_ylabel("Cumplimiento (%)")
    ax.set_ylim(0, tope * 1.1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(handles=[
        Patch(color=COLORES["VERDE"], label=f"Verde: {umbral_verde} % o más"),
        Patch(color=COLORES["AMARILLO"], label=f"Amarillo: {umbral_amarillo} % a {umbral_verde} %"),
        Patch(color=COLORES["ROJO"], label=f"Rojo: menos de {umbral_amarillo} % (no alcanza)"),
    ], loc="upper right", frameon=False)

    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo
