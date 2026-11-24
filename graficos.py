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


def graficar_alertas(productos, coberturas, alertas, umbral_verde=30,
                     umbral_amarillo=20, archivo="alertas.png"):
    """
    Dibuja un grafico de barras con los dias de cobertura de cada producto,
    pintando cada barra con el color de su alerta y marcando los umbrales.

    Parametros:
        productos: nombres de los productos (eje horizontal).
        coberturas: dias de cobertura de cada producto (alto de cada barra).
        alertas: "VERDE", "AMARILLO" o "ROJO" para cada producto.
        umbral_verde, umbral_amarillo: lineas de referencia en dias.
        archivo: ruta del PNG que se genera.

    Retorna:
        La ruta del archivo generado.
    """
    if not (len(productos) == len(coberturas) == len(alertas)):
        raise ValueError("Productos, coberturas y alertas deben tener el mismo largo.")

    # Una cobertura infinita (producto sin demanda) se dibuja con un tope visible
    finitas = [c for c in coberturas if c != float("inf")]
    tope = max(finitas + [umbral_verde]) * 1.25
    alturas = [min(c, tope) for c in coberturas]
    colores = [COLORES[a] for a in alertas]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.bar(productos, alturas, color=colores, width=0.6)

    # Lineas de los umbrales
    ax.axhline(umbral_verde, color=COLORES["VERDE"], linestyle="--", linewidth=1, zorder=0)
    ax.axhline(umbral_amarillo, color=COLORES["ROJO"], linestyle="--", linewidth=1, zorder=0)

    # Dias sobre cada barra
    for barra, dias in zip(barras, coberturas):
        texto = "sin demanda" if dias == float("inf") else f"{dias:.1f} días".replace(".", ",")
        ax.annotate(texto, (barra.get_x() + barra.get_width() / 2, barra.get_height()),
                    ha="center", va="bottom", xytext=(0, 4), textcoords="offset points",
                    bbox=dict(facecolor="white", edgecolor="none", pad=1))

    ax.set_title("Semáforo de stock: días que alcanza el stock en bodega")
    ax.set_ylabel("Días de cobertura")
    ax.set_ylim(0, tope * 1.1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(handles=[
        Patch(color=COLORES["VERDE"], label=f"Verde: {umbral_verde} días o más"),
        Patch(color=COLORES["AMARILLO"], label=f"Amarillo: {umbral_amarillo} a {umbral_verde} días"),
        Patch(color=COLORES["ROJO"], label=f"Rojo: menos de {umbral_amarillo} días"),
    ], loc="upper right", frameon=False)

    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo
