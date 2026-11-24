# OptiMat

Prototipo en Python que centraliza el inventario de una pyme de retail tecnológico
con varias sucursales y calcula automáticamente cuántas unidades despachar a cada
una y cuánto cuesta ese despacho. Usa datos de ejemplo (sin base de datos ni interfaz gráfica).

## Archivos

- `datos.py`: datos de ejemplo (productos, sucursales, capacidad, stock, tarifas, historial de ventas).
- `calculos.py`: funciones matemáticas.
- `main.py`: ejecuta todo e imprime el reporte.
- `test_calculos.py`: pruebas con un caso pequeño calculado a mano.

## Instalación y ejecución

```bash
pip install -r requirements.txt
python main.py
```

Para correr las pruebas (requiere `pytest`):

```bash
pip install pytest
python -m pytest
```

## Conceptos matemáticos

| Función | Concepto | Qué hace |
|---|---|---|
| `calcular_reposicion` | Resta de matrices | R = Capacidad − Stock (filas = productos, columnas = sucursales) |
| `calcular_costos` | Producto matriz × vector | Costos = R · t (t = tarifa de flete por sucursal); el total es la suma de las componentes |
| `proyectar_demanda` | Sumatoria | Demanda = (1/n) · Σ ventas, calculada con un ciclo `for` acumulativo |
| `detectar_riesgo_quiebre` | Sumatoria por fila | Si Σ stock del producto en todas las sucursales < demanda proyectada, hay riesgo de quiebre |
