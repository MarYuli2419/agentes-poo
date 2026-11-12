# Revisión final del proyecto

**Fecha:** 2026-11-12
**Alcance:** código de `src/`, pruebas de `tests/`, diseño de `docs/diseno.md`,
reporte de pruebas y documentación del repositorio.

No se modificó ningún archivo de `src/` ni de `tests/` durante la revisión.

## 1. Checklist de revisión

| Criterio | Resultado | Evidencia |
|---|---|---|
| Cada clase de `docs/diseno.md` existe en `src/` | Cumple | `Libro`, `Socio`, `Prestamo`, `Biblioteca` y la jerarquía de excepciones están implementados. |
| Los atributos están encapsulados | Cumple | Atributos privados con `_`, acceso mediante `@property` y listas expuestas como tuplas. |
| Hay docstrings en clases y métodos públicos | Cumple | Todas las clases y métodos públicos documentan propósito, parámetros y excepciones. |
| Las entradas se validan | Cumple con observaciones | Los constructores validan tipos y rangos. Ver observación 1. |
| No hay código repetido que deba extraerse | Cumple con observación | `_validar_texto` está duplicado en `Libro` y `Socio`. Ver observación 3. |
| Todas las pruebas pasan | Cumple | 100 pruebas ejecutadas, 100 aprobadas, 0 fallidas. |
| El programa se ejecuta sin errores | Cumple | `python -X utf8 src/main.py` termina correctamente. |

## 2. Lo que está bien

1. **El código sigue el diseño.** Las cuatro clases tienen una responsabilidad clara:
   `Libro` controla ejemplares, `Socio` sus préstamos activos, `Prestamo` sus fechas y
   `Biblioteca` coordina las operaciones.
2. **La consistencia del estado está centralizada.** `Biblioteca` es la única fachada que
   modifica disponibilidad, préstamos activos e historial, lo que evita estados
   inconsistentes entre libro, socio y préstamo.
3. **Las pruebas son sólidas y deterministas.** Se cubren casos normales, límite y de error;
   las fechas se inyectan explícitamente y las 100 pruebas pasan en 0,004 s.
4. **La documentación es clara.** El diseño, el reporte de pruebas y el README explican el
   sistema, sus reglas y cómo ejecutarlo.

## 3. Observaciones encontradas

### Observación 1: validación incompleta en `Socio.registrar_prestamo`

- **Archivo:** `src/socio.py`
- **Descripción:** el método añade cualquier objeto a `_prestamos_activos` sin comprobar que
  sea una instancia de `Prestamo` ni que el préstamo pertenezca a ese socio. En el flujo
  normal solo lo llama `Biblioteca` con datos correctos, pero es un método público.
- **Sugerencia:** validar el tipo y la pertenencia antes de agregar el préstamo, por ejemplo
  con una importación local de `Prestamo` para evitar el ciclo de imports, y añadir pruebas
  para un objeto inválido y para un préstamo de otro socio.
- **Impacto:** bajo; no afecta al flujo actual coordinado por `Biblioteca`.

### Observación 2: validación de tipo en las búsquedas

- **Archivo:** `src/biblioteca.py`
- **Descripción:** `buscar_libro` y `buscar_socio` no validan que el identificador sea texto.
  Un valor no hashable, como una lista, provoca `TypeError` en lugar de `ValueError` o
  `EntidadNoEncontradaError`.
- **Sugerencia:** validar que `isbn` y `numero` sean cadenas no vacías antes de buscar.
- **Impacto:** bajo; los llamadores actuales siempre pasan cadenas.

### Observación 3: pequeña duplicación de validación

- **Archivos:** `src/libro.py` y `src/socio.py`
- **Descripción:** ambos módulos repiten el método `_validar_texto`.
- **Sugerencia:** si el proyecto crece, extraer una función auxiliar compartida o una clase
  base de validación. Para el tamaño actual no es bloqueante.
- **Impacto:** muy bajo; no afecta al comportamiento.

### Observación 4: concordancia gramatical en `Biblioteca.__str__`

- **Archivo:** `src/biblioteca.py`
- **Descripción:** con un único préstamo activo, el texto genera `"1 préstamos activos"`.
- **Sugerencia:** usar singular cuando el conteo sea 1.
- **Impacto:** cosmético.

### Observación 5: README incompleto (corregido)

- **Archivo:** `README.md`
- **Descripción:** el README describía el sistema agéntico, pero no el programa de biblioteca
  ni cómo ejecutarlo y probarlo.
- **Acción:** se actualizó con qué hace el programa, cómo ejecutarlo, cómo correr las
  pruebas, la estructura de carpetas y el diagrama de clases.
- **Estado:** resuelto en esta revisión.

## 4. Verificación ejecutada

```text
python -m unittest discover -s tests -v
Ran 100 tests in 0.004s
OK
```

```text
python -X utf8 src/main.py
```

La demostración se ejecutó sin errores y mostró préstamos, vencimientos, errores controlados
por límite y disponibilidad, devoluciones con retraso y actualización correcta de la
disponibilidad.

## 5. Veredicto

**Aprobado.**

La implementación cumple el diseño, respeta el encapsulamiento, valida los datos principales
y pasa la totalidad de las pruebas. Las observaciones 1 a 4 son mejoras menores no
bloqueantes; la observación 5 ya fue corregida con la actualización del README.

Si se desea una versión más estricta antes de una entrega futura, se recomienda abordar
primero la observación 1 y añadir pruebas específicas para esos casos límite.
