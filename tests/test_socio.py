"""Pruebas de la clase Socio."""

import unittest
from datetime import date

from src.excepciones import PrestamoInvalidoError
from src.libro import Libro
from src.prestamo import Prestamo
from src.socio import (
    DIAS_PRESTAMO_POR_DEFECTO,
    LIMITE_PRESTAMOS_POR_DEFECTO,
    Socio,
)


class TestSocio(unittest.TestCase):
    """Verifica la creación del socio y la gestión de sus préstamos activos."""

    def setUp(self):
        self.socio = Socio("S001", "Ana Pérez", "ana@example.com")
        self.libro = Libro("978-1", "Título", "Autor", 2)

    def _crear_prestamo(self, isbn: str = "978-1") -> Prestamo:
        if isbn == self.libro.isbn:
            libro = self.libro
        else:
            libro = Libro(isbn, "Otro título", "Otro autor", 1)
        return Prestamo(libro, self.socio, date(2026, 1, 1))

    def test_constructor_datos_validos_crea_socio_con_valores_por_defecto(self):
        self.assertEqual(self.socio.numero, "S001")
        self.assertEqual(self.socio.nombre, "Ana Pérez")
        self.assertEqual(self.socio.email, "ana@example.com")
        self.assertEqual(
            self.socio.limite_prestamos,
            LIMITE_PRESTAMOS_POR_DEFECTO,
        )
        self.assertEqual(
            self.socio.dias_prestamo,
            DIAS_PRESTAMO_POR_DEFECTO,
        )
        self.assertEqual(self.socio.prestamos_activos, ())

    def test_constructor_limite_y_dias_personalizados(self):
        socio = Socio(
            "S002",
            "Luis",
            "luis@example.com",
            limite_prestamos=1,
            dias_prestamo=7,
        )
        self.assertEqual(socio.limite_prestamos, 1)
        self.assertEqual(socio.dias_prestamo, 7)

    def test_constructor_numero_vacio_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Socio("", "Ana", "ana@example.com")

    def test_constructor_nombre_vacio_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Socio("S001", "", "ana@example.com")

    def test_constructor_email_sin_arroba_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Socio("S001", "Ana", "ana.example.com")

    def test_constructor_email_sin_punto_en_dominio_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Socio("S001", "Ana", "ana@example")

    def test_constructor_email_no_texto_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Socio("S001", "Ana", 123)

    def test_constructor_limite_cero_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Socio("S001", "Ana", "ana@example.com", limite_prestamos=0)

    def test_constructor_dias_cero_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Socio("S001", "Ana", "ana@example.com", dias_prestamo=0)

    def test_constructor_limite_booleano_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Socio("S001", "Ana", "ana@example.com", limite_prestamos=True)

    def test_puede_pedir_prestamo_sin_prestamos_es_true(self):
        self.assertTrue(self.socio.puede_pedir_prestamo())

    def test_puede_pedir_prestamo_al_alcanzar_limite_es_false(self):
        socio = Socio(
            "S002",
            "Luis",
            "luis@example.com",
            limite_prestamos=1,
        )
        prestamo = Prestamo(self.libro, socio, date(2026, 1, 1))
        socio.registrar_prestamo(prestamo)
        self.assertFalse(socio.puede_pedir_prestamo())

    def test_registrar_prestamo_valido_lo_agrega_a_la_tupla(self):
        prestamo = self._crear_prestamo()
        self.socio.registrar_prestamo(prestamo)
        self.assertEqual(self.socio.prestamos_activos, (prestamo,))

    def test_registrar_prestamo_duplicado_lanza_prestamo_invalido(self):
        prestamo = self._crear_prestamo()
        self.socio.registrar_prestamo(prestamo)
        with self.assertRaises(PrestamoInvalidoError):
            self.socio.registrar_prestamo(prestamo)

    def test_registrar_devolucion_prestamo_activo_lo_quita(self):
        prestamo = self._crear_prestamo()
        self.socio.registrar_prestamo(prestamo)
        self.socio.registrar_devolucion(prestamo)
        self.assertEqual(self.socio.prestamos_activos, ())

    def test_registrar_devolucion_prestamo_no_registrado_lanza_prestamo_invalido(self):
        prestamo = self._crear_prestamo()
        with self.assertRaises(PrestamoInvalidoError):
            self.socio.registrar_devolucion(prestamo)

    def test_tiene_prestamo_activo_con_isbn_registrado_es_true(self):
        prestamo = self._crear_prestamo()
        self.socio.registrar_prestamo(prestamo)
        self.assertTrue(self.socio.tiene_prestamo_activo("978-1"))

    def test_tiene_prestamo_activo_con_isbn_distinto_es_false(self):
        prestamo = self._crear_prestamo()
        self.socio.registrar_prestamo(prestamo)
        self.assertFalse(self.socio.tiene_prestamo_activo("978-2"))

    def test_prestamos_activos_es_una_tupla_inmutable(self):
        self.assertIsInstance(self.socio.prestamos_activos, tuple)
        with self.assertRaises(AttributeError):
            self.socio.prestamos_activos = ()

    def test_str_incluye_numero_y_limite(self):
        texto = str(self.socio)
        self.assertIn("S001", texto)
        self.assertIn("3", texto)
        self.assertIn("préstamos activos", texto)


if __name__ == "__main__":
    unittest.main()
