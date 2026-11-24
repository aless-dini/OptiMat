# OptiMat

Prototipo en Python para una pyme de retail tecnológico que vende desde una bodega
a varios clientes. Calcula cuántas unidades faltan por despachar a cada cliente,
cuánto cuesta ese despacho, si el stock de la bodega alcanza y qué productos
tienen riesgo de quiebre de stock, con un semáforo de alertas y su gráfico.
Usa datos de ejemplo (sin base de datos ni interfaz gráfica).

## Archivos

- `datos.py`: datos de ejemplo (productos, clientes, pedidos, entregas, tarifas, stock en bodega, ventas de 6 meses en un arreglo de 3 dimensiones y umbrales del semáforo).
- `calculos.py`: funciones matemáticas.
- `graficos.py`: gráfico del semáforo de stock con Matplotlib.
- `main.py`: ejecuta todo, imprime el reporte y guarda el gráfico en `alertas.png`.
- `test_calculos.py`: pruebas con un caso pequeño calculado a mano.
- `docs/`: tablas de la Etapa 2 en PDF y Word, y la presentación de la Etapa 3.

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
| `calcular_reposicion` | Resta de matrices | R = Pedidos − Entregado (filas = productos, columnas = clientes) |
| `calcular_costos` | Producto matriz × vector | Costos = R · t (t = tarifa de flete por cliente); el total es la suma de las componentes |
| `verificar_despacho` | Sumatoria por fila | Σ de lo pendiente de cada producto en todos los clientes, comparado con el stock en bodega |
| `proyectar_demanda` | Sumatoria | Demanda = (1/n) · Σ ventas, calculada con un ciclo `for` acumulativo |
| `detectar_riesgo_quiebre` | Comparación | Si el stock en bodega < demanda proyectada, hay riesgo de quiebre |
| `resumir_ventas` | Arreglo multidimensional y sumatoria por eje | V tiene 3 índices (producto, cliente, mes); Σ sobre los clientes da la matriz productos × meses y Σ sobre los meses da la matriz productos × clientes |
| `calcular_cobertura` | Proporción | Días de cobertura = stock / (demanda mensual / 30) |
| `clasificar_alertas` | Desigualdades | Verde si cobertura ≥ 30 días, amarillo si 20 ≤ cobertura < 30, rojo si cobertura < 20 |
