"""Modelo de un préstamo de libro."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from .excepciones import PrestamoInvalidoError
from .libro import Libro
from .socio import Socio


class Prestamo:
    """Representa el préstamo de un libro a un socio."""

    def __init__(
        self,
        libro: Libro,
        socio: Socio,
        fecha_prestamo: date | None = None,
        dias_prestamo: int | None = None,
    ) -> None:
        """Crea un préstamo y calcula su fecha límite.

        Args:
            libro: Libro prestado.
            socio: Socio que recibe el libro.
            fecha_prestamo: Fecha del préstamo. Si es None, se usa la fecha
                actual.
            dias_prestamo: Duración en días. Si es None, se usa la del socio.

        Raises:
            ValueError: Si el libro, el socio, la fecha o los días no son
                válidos.
        """
        if not isinstance(libro, Libro):
            raise ValueError("El libro debe ser una instancia de Libro")
        if not isinstance(socio, Socio):
            raise ValueError("El socio debe ser una instancia de Socio")

        fecha = self._validar_fecha(
            fecha_prestamo if fecha_prestamo is not None else date.today(),
            "fecha_prestamo",
        )
        dias = dias_prestamo if dias_prestamo is not None else socio.dias_prestamo
        if not isinstance(dias, int) or isinstance(dias, bool):
            raise ValueError("Los días de préstamo deben ser un número entero")
        if dias < 1:
            raise ValueError("Los días de préstamo deben ser al menos 1")

        self._libro = libro
        self._socio = socio
        self._fecha_prestamo = fecha
        self._fecha_limite = fecha + timedelta(days=dias)
        self._fecha_devolucion: date | None = None

    @staticmethod
    def _validar_fecha(valor: date, campo: str) -> date:
        if not isinstance(valor, date) or isinstance(valor, datetime):
            raise ValueError(f"El campo '{campo}' debe ser una fecha válida")
        return valor

    @property
    def libro(self) -> Libro:
        """Libro prestado."""
        return self._libro

    @property
    def socio(self) -> Socio:
        """Socio que recibió el libro."""
        return self._socio

    @property
    def fecha_prestamo(self) -> date:
        """Fecha en que se realizó el préstamo."""
        return self._fecha_prestamo

    @property
    def fecha_limite(self) -> date:
        """Fecha límite para devolver el libro."""
        return self._fecha_limite

    @property
    def fecha_devolucion(self) -> date | None:
        """Fecha de devolución, o None si el préstamo sigue activo."""
        return self._fecha_devolucion

    def esta_activo(self) -> bool:
        """Indica si el préstamo aún no ha sido devuelto."""
        return self._fecha_devolucion is None

    def dias_retraso(self, hoy: date | None = None) -> int:
        """Calcula los días de retraso del préstamo.

        Si el préstamo ya fue devuelto, se compara la fecha de devolución con
        la fecha límite. Si sigue activo, se compara ``hoy`` (o la fecha
        actual) con la fecha límite.

        Args:
            hoy: Fecha de referencia para préstamos activos.

        Returns:
            Número de días de retraso; 0 si no hay retraso.

        Raises:
            ValueError: Si ``hoy`` no es una fecha válida.
        """
        if hoy is not None:
            self._validar_fecha(hoy, "hoy")

        if self._fecha_devolucion is not None:
            referencia = self._fecha_devolucion
        else:
            referencia = hoy if hoy is not None else date.today()

        return max(0, (referencia - self._fecha_limite).days)

    def esta_vencido(self, hoy: date | None = None) -> bool:
        """Indica si el préstamo tiene algún día de retraso."""
        return self.dias_retraso(hoy) > 0

    def devolver(self, hoy: date | None = None) -> None:
        """Registra la devolución del préstamo.

        Args:
            hoy: Fecha de devolución. Si es None, se usa la fecha actual.

        Raises:
            PrestamoInvalidoError: Si el préstamo ya fue devuelto.
            ValueError: Si la fecha no es válida o es anterior al préstamo.
        """
        if not self.esta_activo():
            raise PrestamoInvalidoError("El préstamo ya fue devuelto")

        fecha = self._validar_fecha(
            hoy if hoy is not None else date.today(), "fecha_devolucion"
        )
        if fecha < self._fecha_prestamo:
            raise ValueError(
                "La fecha de devolución no puede ser anterior a la fecha "
                "del préstamo"
            )

        self._fecha_devolucion = fecha

    def __str__(self) -> str:
        """Devuelve una representación legible del préstamo."""
        if self.esta_activo():
            estado = "activo"
        else:
            estado = f"devuelto el {self._fecha_devolucion}"
        return (
            f"Préstamo de '{self._libro.titulo}' a {self._socio.nombre}: "
            f"{self._fecha_prestamo} -> {self._fecha_limite} ({estado})"
        )
