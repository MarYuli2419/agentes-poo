"""Fachada de coordinación del sistema de biblioteca."""

from __future__ import annotations

from datetime import date

from .excepciones import (
    EntidadNoEncontradaError,
    LibroNoDisponibleError,
    LimitePrestamosError,
    PrestamoInvalidoError,
)
from .libro import Libro
from .prestamo import Prestamo
from .socio import Socio


class Biblioteca:
    """Coordina el catálogo de libros, los socios y los préstamos."""

    def __init__(self, nombre: str) -> None:
        """Crea una biblioteca vacía.

        Args:
            nombre: Nombre de la biblioteca.

        Raises:
            ValueError: Si el nombre está vacío o no es texto.
        """
        if not isinstance(nombre, str):
            raise ValueError("El nombre de la biblioteca debe ser texto")
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la biblioteca es obligatorio")

        self._nombre = nombre
        self._libros: dict[str, Libro] = {}
        self._socios: dict[str, Socio] = {}
        self._prestamos: list[Prestamo] = []

    @property
    def nombre(self) -> str:
        """Nombre de la biblioteca."""
        return self._nombre

    @property
    def libros(self) -> tuple[Libro, ...]:
        """Copia inmutable del catálogo de libros."""
        return tuple(self._libros.values())

    @property
    def socios(self) -> tuple[Socio, ...]:
        """Copia inmutable del registro de socios."""
        return tuple(self._socios.values())

    @property
    def prestamos(self) -> tuple[Prestamo, ...]:
        """Copia inmutable de todos los préstamos registrados."""
        return tuple(self._prestamos)

    def registrar_libro(self, libro: Libro) -> None:
        """Añade un libro al catálogo.

        Raises:
            ValueError: Si el libro no es válido o su ISBN ya está registrado.
        """
        if not isinstance(libro, Libro):
            raise ValueError("El libro debe ser una instancia de Libro")
        if libro.isbn in self._libros:
            raise ValueError(f"Ya existe un libro con ISBN '{libro.isbn}'")
        self._libros[libro.isbn] = libro

    def registrar_socio(self, socio: Socio) -> None:
        """Añade un socio al registro.

        Raises:
            ValueError: Si el socio no es válido o su número ya está registrado.
        """
        if not isinstance(socio, Socio):
            raise ValueError("El socio debe ser una instancia de Socio")
        if socio.numero in self._socios:
            raise ValueError(f"Ya existe un socio con número '{socio.numero}'")
        self._socios[socio.numero] = socio

    def buscar_libro(self, isbn: str) -> Libro:
        """Busca un libro por ISBN.

        Raises:
            EntidadNoEncontradaError: Si no existe un libro con ese ISBN.
        """
        try:
            return self._libros[isbn]
        except KeyError as exc:
            raise EntidadNoEncontradaError(
                f"No existe un libro con ISBN '{isbn}'"
            ) from exc

    def buscar_socio(self, numero: str) -> Socio:
        """Busca un socio por su número.

        Raises:
            EntidadNoEncontradaError: Si no existe un socio con ese número.
        """
        try:
            return self._socios[numero]
        except KeyError as exc:
            raise EntidadNoEncontradaError(
                f"No existe un socio con número '{numero}'"
            ) from exc

    def prestar(
        self,
        isbn: str,
        numero_socio: str,
        fecha: date | None = None,
    ) -> Prestamo:
        """Registra el préstamo de un ejemplar a un socio.

        Args:
            isbn: ISBN del libro a prestar.
            numero_socio: Número del socio que recibe el libro.
            fecha: Fecha del préstamo. Si es None, se usa la fecha actual.

        Returns:
            El préstamo creado.

        Raises:
            EntidadNoEncontradaError: Si el libro o el socio no existen.
            LibroNoDisponibleError: Si no quedan ejemplares disponibles.
            LimitePrestamosError: Si el socio alcanzó su límite de préstamos.
            PrestamoInvalidoError: Si el socio ya tiene ese libro prestado.
        """
        libro = self.buscar_libro(isbn)
        socio = self.buscar_socio(numero_socio)

        if not libro.hay_disponible():
            raise LibroNoDisponibleError(
                f"No hay ejemplares disponibles de '{libro.titulo}'"
            )
        if not socio.puede_pedir_prestamo():
            raise LimitePrestamosError(
                f"El socio {socio.numero} alcanzó su límite de "
                f"{socio.limite_prestamos} préstamos activos"
            )
        if socio.tiene_prestamo_activo(isbn):
            raise PrestamoInvalidoError(
                f"El socio {socio.numero} ya tiene un préstamo activo de "
                f"'{libro.titulo}'"
            )

        prestamo = Prestamo(libro, socio, fecha_prestamo=fecha)
        libro.prestar_ejemplar()
        socio.registrar_prestamo(prestamo)
        self._prestamos.append(prestamo)
        return prestamo

    def devolver(self, prestamo: Prestamo, fecha: date | None = None) -> int:
        """Registra la devolución de un préstamo.

        Args:
            prestamo: Préstamo a devolver.
            fecha: Fecha de devolución. Si es None, se usa la fecha actual.

        Returns:
            Días de retraso respecto de la fecha límite.

        Raises:
            ValueError: Si el préstamo no es una instancia de Prestamo.
            PrestamoInvalidoError: Si el préstamo no pertenece a la biblioteca
                o ya fue devuelto.
        """
        if not isinstance(prestamo, Prestamo):
            raise ValueError("El préstamo debe ser una instancia de Prestamo")
        if prestamo not in self._prestamos:
            raise PrestamoInvalidoError(
                "El préstamo no pertenece a esta biblioteca"
            )
        if not prestamo.esta_activo():
            raise PrestamoInvalidoError("El préstamo ya fue devuelto")

        prestamo.devolver(fecha)
        prestamo.libro.devolver_ejemplar()
        prestamo.socio.registrar_devolucion(prestamo)
        return prestamo.dias_retraso()

    def prestamos_activos(self) -> list[Prestamo]:
        """Devuelve los préstamos que aún no han sido devueltos."""
        return [prestamo for prestamo in self._prestamos if prestamo.esta_activo()]

    def prestamos_vencidos(self, hoy: date | None = None) -> list[Prestamo]:
        """Devuelve los préstamos activos con retraso a la fecha indicada."""
        return [
            prestamo
            for prestamo in self._prestamos
            if prestamo.esta_activo() and prestamo.esta_vencido(hoy)
        ]

    def historial_socio(self, numero: str) -> list[Prestamo]:
        """Devuelve todos los préstamos de un socio, activos e históricos.

        Raises:
            EntidadNoEncontradaError: Si el socio no existe.
        """
        socio = self.buscar_socio(numero)
        return [
            prestamo
            for prestamo in self._prestamos
            if prestamo.socio is socio
        ]

    def libros_disponibles(self) -> list[Libro]:
        """Devuelve los libros con al menos un ejemplar disponible."""
        return [libro for libro in self._libros.values() if libro.hay_disponible()]

    def __str__(self) -> str:
        """Devuelve una representación legible de la biblioteca."""
        return (
            f"Biblioteca '{self._nombre}' - {len(self._libros)} libros, "
            f"{len(self._socios)} socios, "
            f"{len(self.prestamos_activos())} préstamos activos"
        )
