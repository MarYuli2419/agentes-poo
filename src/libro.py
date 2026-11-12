"""Modelo de un libro con control de ejemplares disponibles."""

from __future__ import annotations

from .excepciones import LibroNoDisponibleError, PrestamoInvalidoError


class Libro:
    """Representa un libro y controla cuántos ejemplares quedan disponibles."""

    def __init__(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        ejemplares_totales: int = 1,
    ) -> None:
        """Crea un libro con sus datos y ejemplares.

        Args:
            isbn: Identificador único del libro.
            titulo: Título del libro.
            autor: Autor del libro.
            ejemplares_totales: Número de copias físicas. Debe ser al menos 1.

        Raises:
            ValueError: Si algún texto está vacío o el número de ejemplares no
                es válido.
        """
        self._isbn = self._validar_texto(isbn, "isbn")
        self._titulo = self._validar_texto(titulo, "titulo")
        self._autor = self._validar_texto(autor, "autor")
        if not isinstance(ejemplares_totales, int) or isinstance(
            ejemplares_totales, bool
        ):
            raise ValueError("Los ejemplares totales deben ser un número entero")
        if ejemplares_totales < 1:
            raise ValueError("Los ejemplares totales deben ser al menos 1")

        self._ejemplares_totales = ejemplares_totales
        self._ejemplares_disponibles = ejemplares_totales

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str):
            raise ValueError(f"El campo '{campo}' debe ser texto")
        valor = valor.strip()
        if not valor:
            raise ValueError(f"El campo '{campo}' es obligatorio")
        return valor

    @property
    def isbn(self) -> str:
        """ISBN del libro."""
        return self._isbn

    @property
    def titulo(self) -> str:
        """Título del libro."""
        return self._titulo

    @property
    def autor(self) -> str:
        """Autor del libro."""
        return self._autor

    @property
    def ejemplares_totales(self) -> int:
        """Número total de ejemplares del libro."""
        return self._ejemplares_totales

    @property
    def ejemplares_disponibles(self) -> int:
        """Número de ejemplares disponibles en este momento."""
        return self._ejemplares_disponibles

    def hay_disponible(self) -> bool:
        """Indica si queda al menos un ejemplar disponible."""
        return self._ejemplares_disponibles > 0

    def prestar_ejemplar(self) -> None:
        """Descuenta un ejemplar disponible.

        Raises:
            LibroNoDisponibleError: Si no quedan ejemplares disponibles.
        """
        if not self.hay_disponible():
            raise LibroNoDisponibleError(
                f"No hay ejemplares disponibles de '{self._titulo}'"
            )
        self._ejemplares_disponibles -= 1

    def devolver_ejemplar(self) -> None:
        """Incrementa un ejemplar disponible.

        Raises:
            PrestamoInvalidoError: Si todos los ejemplares ya están disponibles.
        """
        if self._ejemplares_disponibles >= self._ejemplares_totales:
            raise PrestamoInvalidoError(
                f"Todos los ejemplares de '{self._titulo}' ya están disponibles"
            )
        self._ejemplares_disponibles += 1

    def __str__(self) -> str:
        """Devuelve una representación legible del libro."""
        return (
            f"{self._titulo} ({self._autor}) - ISBN {self._isbn} - "
            f"{self._ejemplares_disponibles}/{self._ejemplares_totales} disponibles"
        )
