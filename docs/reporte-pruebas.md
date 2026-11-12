# Reporte de pruebas

## 1. Alcance

Se probó la implementación de `src/` contra el diseño de `docs/diseno.md`:

- `src/libro.py` → `Libro`
- `src/socio.py` → `Socio`
- `src/prestamo.py` → `Prestamo`
- `src/biblioteca.py` → `Biblioteca`
- `src/excepciones.py` → jerarquía de errores de negocio
- `src/main.py` → demostración ejecutable

No se modificó ningún archivo de `src/` durante las pruebas.

## 2. Entorno y ejecución

| Elemento | Valor |
|---|---|
| Python | 3.13.14 |
| Framework | `unittest` (incluido en Python) |
| pytest | No instalado en el entorno |
| Comando | `python -m unittest discover -s tests -v` |
| Fecha de ejecución | 2026-11-12 |
| Duración | 0,006 s |

## 3. Resultado global

| Métrica | Cantidad |
|---|---|
| Pruebas ejecutadas | 100 |
| Pruebas aprobadas | 100 |
| Pruebas fallidas | 0 |
| Errores | 0 |
| Resultado final | **OK** |

## 4. Resultados por archivo

| Prueba (archivo) | Ejecutadas | Aprobadas | Fallidas | Observación |
|---|---:|---:|---:|---|
| `tests/test_biblioteca.py` | 36 | 36 | 0 | Registro, búsqueda, préstamo, devolución e informes. |
| `tests/test_libro.py` | 16 | 16 | 0 | Creación, disponibilidad y control de ejemplares. |
| `tests/test_prestamo.py` | 28 | 28 | 0 | Fechas, vencimiento, retraso y devolución. |
| `tests/test_socio.py` | 20 | 20 | 0 | Validaciones, límites y préstamos activos. |
| **Total** | **100** | **100** | **0** | **Todos los casos pasaron.** |

## 5. Cobertura por clase

| Clase | Casos normales | Casos límite | Casos de error |
|---|---|---|---|
| `Libro` | Creación con varios ejemplares, préstamo y devolución, disponibilidad. | Un solo ejemplar, devolver todo lo prestado. | Textos vacíos, ejemplares 0/negativos/no enteros, préstamo sin disponibilidad, doble devolución. |
| `Socio` | Valores por defecto, límites personalizados, registro y devolución de préstamos. | Alcanzar exactamente el límite, límite booleano. | Número/nombre vacíos, email inválido, límites menores que 1, préstamo duplicado, devolución no registrada. |
| `Prestamo` | Cálculo de fecha límite, estado activo, vencimiento y retraso. | Fecha límite exacta, devolución el mismo día, cero días de retraso. | Libro/socio/fecha inválidos, días 0/negativos/booleanos, doble devolución, devolución anterior al préstamo. |
| `Biblioteca` | Registro, búsqueda, préstamo, devolución, préstamos vencidos, historial y disponibilidad. | Varios ejemplares del mismo libro, límite exacto del socio, préstamo en la fecha límite. | Duplicados, entidades inexistentes, libro sin ejemplares, préstamo repetido, devolución ajena o doble, fecha inválida. |

## 6. Verificación de la demostración

Se ejecutó `python -X utf8 src/main.py` y el programa terminó sin errores. La salida mostró:

- creación de dos libros y dos socios,
- dos préstamos con fechas deterministas,
- dos préstamos vencidos en la fecha consultada,
- errores controlados por falta de ejemplares y por límite de socio,
- devoluciones con 0 y 4 días de retraso,
- actualización correcta de la disponibilidad y del historial.

## 7. Fallos y acciones

No hubo pruebas fallidas ni errores. No se requiere ninguna corrección por parte del agente **desarrollador**.

## 8. Conclusión

La implementación cumple el diseño y las reglas de negocio:

- las validaciones de datos lanzan `ValueError`,
- los errores de dominio usan la jerarquía `BibliotecaError`,
- se respetan los límites de préstamos y la disponibilidad,
- las devoluciones actualizan de forma consistente libro, socio y biblioteca,
- los cálculos de fecha límite y retraso son correctos.

El código queda listo para la revisión final del agente **revisor**.
