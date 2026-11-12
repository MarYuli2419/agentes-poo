"""Modelo de un socio de la biblioteca."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .excepciones import PrestamoInvalidoError

if TYPE_CHECKING:
    from .prestamo import Prestamo


LIMITE_PRESTAMOS_POR_DEFECTO = 3
DIAS_PRESTAMO_POR_DEFECTO = 14

_PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Socio:
    """Representa a un socio y controla sus préstamos activos."""

    def __init__(
        self,
        numero: str,
        nombre: str,
        email: str,
        limite_prestamos: int = LIMITE_PRESTAMOS_POR_DEFECTO,
        dias_prestamo: int = DIAS_PRESTAMO_POR_DEFECTO,
    ) -> None:
        """Crea un socio con sus datos y sus límites de préstamo.

        Args:
            numero: Identificador único del socio.
            nombre: Nombre completo del socio.
            email: Correo electrónico de contacto.
            limite_prestamos: Máximo de préstamos activos permitidos.
            dias_prestamo: Plazo en días de cada préstamo.

        Raises:
            ValueError: Si algún dato no es válido.
        """
        self._numero = self._validar_texto(numero, "numero")
        self._nombre = self._validar_texto(nombre, "nombre")
        self._email = self._validar_email(email)
        self._limite_prestamos = self._validar_entero_positivo(
            limite_prestamos, "limite_prestamos"
        )
        self._dias_prestamo = self._validar_entero_positivo(
            dias_prestamo, "dias_prestamo"
        )
        self._prestamos_activos: list[Prestamo] = []

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str):
            raise ValueError(f"El campo '{campo}' debe ser texto")
        valor = valor.strip()
        if not valor:
            raise ValueError(f"El campo '{campo}' es obligatorio")
        return valor

    @staticmethod
    def _validar_email(email: str) -> str:
        if not isinstance(email, str):
            raise ValueError("El email debe ser texto")
        email = email.strip()
        if not _PATRON_EMAIL.fullmatch(email):
            raise ValueError("El email no tiene un formato válido")
        return email

    @staticmethod
    def _validar_entero_positivo(valor: int, campo: str) -> int:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError(f"El campo '{campo}' debe ser un número entero")
        if valor < 1:
            raise ValueError(f"El campo '{campo}' debe ser al menos 1")
        return valor

    @property
    def numero(self) -> str:
        """Número único del socio."""
        return self._numero

    @property
    def nombre(self) -> str:
        """Nombre completo del socio."""
        return self._nombre

    @property
    def email(self) -> str:
        """Correo electrónico del socio."""
        return self._email

    @property
    def limite_prestamos(self) -> int:
        """Máximo de préstamos activos permitidos."""
        return self._limite_prestamos

    @property
    def dias_prestamo(self) -> int:
        """Plazo en días de cada préstamo."""
        return self._dias_prestamo

    @property
    def prestamos_activos(self) -> tuple[Prestamo, ...]:
        """Copia inmutable de los préstamos activos del socio."""
        return tuple(self._prestamos_activos)

    def puede_pedir_prestamo(self) -> bool:
        """Indica si el socio aún no alcanzó su límite de préstamos."""
        return len(self._prestamos_activos) < self._limite_prestamos

    def registrar_prestamo(self, prestamo: Prestamo) -> None:
        """Añade un préstamo a la lista de préstamos activos.

        Raises:
            PrestamoInvalidoError: Si el préstamo ya estaba registrado.
        """
        if prestamo in self._prestamos_activos:
            raise PrestamoInvalidoError(
                "El préstamo ya está registrado para este socio"
            )
        self._prestamos_activos.append(prestamo)

    def registrar_devolucion(self, prestamo: Prestamo) -> None:
        """Quita un préstamo de la lista de préstamos activos.

        Raises:
            PrestamoInvalidoError: Si el préstamo no estaba activo para el socio.
        """
        if prestamo not in self._prestamos_activos:
            raise PrestamoInvalidoError(
                "El préstamo no está activo para este socio"
            )
        self._prestamos_activos.remove(prestamo)

    def tiene_prestamo_activo(self, isbn: str) -> bool:
        """Indica si el socio tiene un préstamo activo con ese ISBN."""
        return any(
            prestamo.libro.isbn == isbn for prestamo in self._prestamos_activos
        )

    def __str__(self) -> str:
        """Devuelve una representación legible del socio."""
        return (
            f"Socio {self._numero} - {self._nombre} ({self._email}) - "
            f"{len(self._prestamos_activos)}/{self._limite_prestamos} "
            "préstamos activos"
        )
