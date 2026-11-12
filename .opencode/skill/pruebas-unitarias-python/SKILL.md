---
name: pruebas-unitarias-python
description: Cómo diseñar, escribir y ejecutar pruebas unitarias en Python con pytest o unittest, incluyendo el reporte de resultados.
---

# Skill: pruebas unitarias en Python

## Cuándo usarla
Cuando haya código en `src/` que deba verificarse.

## Pasos
1. Por cada clase, crea `tests/test_<clase>.py`.
2. Para cada método público escribe al menos:
   - un **caso normal**,
   - un **caso límite** (cero, vacío, máximo),
   - un **caso de error** (debe lanzar la excepción esperada).
3. Nombra las pruebas así: `test_<metodo>_<situacion>_<resultado>`.
4. Ejecuta: `python -m pytest -v` (o `python -m unittest discover -s tests -v`).
5. Registra los resultados en `docs/reporte-pruebas.md`.

## Ejemplo
```python
import pytest
from src.cuenta import Cuenta

def test_depositar_monto_valido_aumenta_saldo():
    c = Cuenta("Ana", 100)
    c.depositar(50)
    assert c.saldo == 150

def test_depositar_monto_negativo_lanza_error():
    c = Cuenta("Ana")
    with pytest.raises(ValueError):
        c.depositar(-5)
```

## Formato del reporte
| Prueba | Resultado | Observación |
|---|---|---|

Cierra con el total de pruebas, aprobadas y fallidas.
