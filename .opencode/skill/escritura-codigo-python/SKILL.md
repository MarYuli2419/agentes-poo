---
name: escritura-codigo-python
description: Convenciones para escribir código Python orientado a objetos limpio, con encapsulamiento, docstrings y validaciones.
---

# Skill: escritura de código Python (POO)

## Cuándo usarla
Cuando haya que implementar clases a partir de un diseño.

## Estructura
```
src/
├── __init__.py
├── modelo_a.py     # una clase por archivo
├── modelo_b.py
└── main.py         # punto de entrada
```

## Convenciones
- Clases en `PascalCase`, métodos y variables en `snake_case`.
- Atributos internos con guion bajo (`self._saldo`) y acceso con `@property`.
- Constructor `__init__` que valide los datos recibidos.
- `__str__` en las clases principales para imprimirlas de forma legible.
- Docstrings en español: qué hace, parámetros y excepciones.
- Anotaciones de tipo en los parámetros y retornos.

## Plantilla de clase
```python
class Cuenta:
    """Representa una cuenta bancaria simple."""

    def __init__(self, titular: str, saldo: float = 0.0) -> None:
        if not titular:
            raise ValueError("El titular es obligatorio")
        self._titular = titular
        self._saldo = saldo

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float) -> None:
        """Suma el monto al saldo. Lanza ValueError si el monto no es positivo."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self._saldo += monto
```

## Antes de terminar
- Ejecuta `python src/main.py` y confirma que no hay errores.
- Verifica que cada clase del diseño existe.
