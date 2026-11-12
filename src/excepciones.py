"""Excepciones de negocio del sistema de biblioteca."""


class BibliotecaError(Exception):
    """Error base de todas las reglas de negocio de la biblioteca."""


class LibroNoDisponibleError(BibliotecaError):
    """Se lanza al intentar prestar un libro sin ejemplares disponibles."""


class LimitePrestamosError(BibliotecaError):
    """Se lanza cuando un socio alcanza su límite de préstamos activos."""


class EntidadNoEncontradaError(BibliotecaError):
    """Se lanza cuando no se encuentra un libro o un socio."""


class PrestamoInvalidoError(BibliotecaError):
    """Se lanza cuando una operación sobre un préstamo no es válida."""
