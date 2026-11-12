"""Demostración del sistema de biblioteca."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.biblioteca import Biblioteca
from src.excepciones import BibliotecaError
from src.libro import Libro
from src.socio import Socio


def main() -> None:
    """Ejecuta una demostración con libros, socios y préstamos."""
    biblioteca = Biblioteca("Biblioteca Central")

    cien_anios = Libro(
        "978-0307474728",
        "Cien años de soledad",
        "Gabriel García Márquez",
        2,
    )
    principito = Libro(
        "978-0156012195",
        "El principito",
        "Antoine de Saint-Exupéry",
        1,
    )

    ana = Socio("S001", "Ana Pérez", "ana@example.com")
    luis = Socio("S002", "Luis Gómez", "luis@example.com", limite_prestamos=1)

    biblioteca.registrar_libro(cien_anios)
    biblioteca.registrar_libro(principito)
    biblioteca.registrar_socio(ana)
    biblioteca.registrar_socio(luis)

    print(biblioteca)
    print(
        "Libros disponibles:",
        [libro.titulo for libro in biblioteca.libros_disponibles()],
    )
    print()

    prestamo_ana = biblioteca.prestar(
        cien_anios.isbn, ana.numero, date(2026, 1, 10)
    )
    prestamo_luis = biblioteca.prestar(
        principito.isbn, luis.numero, date(2026, 1, 12)
    )

    print(prestamo_ana)
    print(prestamo_luis)
    print(
        "Libros disponibles:",
        [libro.titulo for libro in biblioteca.libros_disponibles()],
    )
    print()

    for prestamo in biblioteca.prestamos_vencidos(date(2026, 1, 27)):
        print(f"Vencido: {prestamo}")
    print()

    try:
        biblioteca.prestar(principito.isbn, ana.numero, date(2026, 1, 13))
    except BibliotecaError as error:
        print(f"Error controlado: {error}")

    try:
        biblioteca.prestar(cien_anios.isbn, luis.numero, date(2026, 1, 13))
    except BibliotecaError as error:
        print(f"Error controlado: {error}")
    print()

    retraso_ana = biblioteca.devolver(prestamo_ana, date(2026, 1, 24))
    retraso_luis = biblioteca.devolver(prestamo_luis, date(2026, 1, 30))
    print(f"Devolución de {ana.nombre}: {retraso_ana} días de retraso")
    print(f"Devolución de {luis.nombre}: {retraso_luis} días de retraso")
    print(f"Préstamos activos: {len(biblioteca.prestamos_activos())}")
    print(
        f"Historial de {ana.nombre}: "
        f"{len(biblioteca.historial_socio(ana.numero))} préstamo(s)"
    )
    print(
        "Libros disponibles:",
        [libro.titulo for libro in biblioteca.libros_disponibles()],
    )


if __name__ == "__main__":
    main()
