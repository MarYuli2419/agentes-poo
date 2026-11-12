"""Pruebas de la clase Prestamo."""

import unittest
from datetime import date, datetime, timedelta

from src.excepciones import PrestamoInvalidoError
from src.libro import Libro
from src.prestamo import Prestamo
from src.socio import Socio


class TestPrestamo(unittest.TestCase):
    """Verifica las fechas, el estado y el retraso de un préstamo."""

    def setUp(self):
        self.libro = Libro("978-1", "Título", "Autor", 1)
        self.socio = Socio("S001", "Ana", "ana@example.com")
        self.fecha = date(2026, 1, 1)

    def _crear(
        self,
        fecha_prestamo: date | None = None,
        dias_prestamo: int | None = None,
    ) -> Prestamo:
        if fecha_prestamo is None:
            fecha_prestamo = self.fecha
        return Prestamo(
            self.libro,
            self.socio,
            fecha_prestamo=fecha_prestamo,
            dias_prestamo=dias_prestamo,
        )

    def test_constructor_fecha_explicita_calcula_fecha_limite(self):
        prestamo = self._crear()
        self.assertEqual(prestamo.fecha_prestamo, self.fecha)
        self.assertEqual(prestamo.fecha_limite, date(2026, 1, 15))
        self.assertIsNone(prestamo.fecha_devolucion)
        self.assertTrue(prestamo.esta_activo())

    def test_constructor_dias_personalizados_calcula_fecha_limite(self):
        prestamo = self._crear(dias_prestamo=7)
        self.assertEqual(prestamo.fecha_limite, date(2026, 1, 8))

    def test_constructor_sin_fecha_usa_fecha_actual_y_calcula_limite(self):
        prestamo = Prestamo(self.libro, self.socio)
        self.assertIsInstance(prestamo.fecha_prestamo, date)
        self.assertEqual(
            prestamo.fecha_limite,
            prestamo.fecha_prestamo + timedelta(days=14),
        )

    def test_constructor_libro_invalido_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Prestamo("no es un libro", self.socio, self.fecha)

    def test_constructor_socio_invalido_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Prestamo(self.libro, "no es un socio", self.fecha)

    def test_constructor_fecha_invalida_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Prestamo(self.libro, self.socio, "2026-01-01")

    def test_constructor_datetime_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Prestamo(self.libro, self.socio, datetime(2026, 1, 1, 10, 0))

    def test_constructor_dias_cero_lanza_value_error(self):
        with self.assertRaises(ValueError):
            self._crear(dias_prestamo=0)

    def test_constructor_dias_negativos_lanza_value_error(self):
        with self.assertRaises(ValueError):
            self._crear(dias_prestamo=-1)

    def test_constructor_dias_booleano_lanza_value_error(self):
        with self.assertRaises(ValueError):
            self._crear(dias_prestamo=True)

    def test_esta_activo_recien_creado_es_true(self):
        prestamo = self._crear()
        self.assertTrue(prestamo.esta_activo())

    def test_esta_activo_tras_devolver_es_false(self):
        prestamo = self._crear()
        prestamo.devolver(date(2026, 1, 10))
        self.assertFalse(prestamo.esta_activo())

    def test_esta_vencido_antes_de_fecha_limite_es_false(self):
        prestamo = self._crear()
        self.assertFalse(prestamo.esta_vencido(date(2026, 1, 14)))

    def test_esta_vencido_en_fecha_limite_es_false(self):
        prestamo = self._crear()
        self.assertFalse(prestamo.esta_vencido(date(2026, 1, 15)))

    def test_esta_vencido_despues_de_fecha_limite_es_true(self):
        prestamo = self._crear()
        self.assertTrue(prestamo.esta_vencido(date(2026, 1, 16)))

    def test_dias_retraso_antes_de_fecha_limite_es_cero(self):
        prestamo = self._crear()
        self.assertEqual(prestamo.dias_retraso(date(2026, 1, 10)), 0)

    def test_dias_retraso_en_fecha_limite_es_cero(self):
        prestamo = self._crear()
        self.assertEqual(prestamo.dias_retraso(date(2026, 1, 15)), 0)

    def test_dias_retraso_despues_de_fecha_limite_cuenta_dias(self):
        prestamo = self._crear()
        self.assertEqual(prestamo.dias_retraso(date(2026, 1, 20)), 5)

    def test_dias_retraso_tras_devolucion_tardia_usa_fecha_devolucion(self):
        prestamo = self._crear()
        prestamo.devolver(date(2026, 1, 20))
        self.assertEqual(prestamo.dias_retraso(date(2026, 2, 1)), 5)

    def test_dias_retraso_con_hoy_invalido_lanza_value_error(self):
        prestamo = self._crear()
        with self.assertRaises(ValueError):
            prestamo.dias_retraso("2026-01-20")

    def test_devolver_fecha_valida_registra_fecha_y_desactiva(self):
        prestamo = self._crear()
        prestamo.devolver(date(2026, 1, 10))
        self.assertEqual(prestamo.fecha_devolucion, date(2026, 1, 10))
        self.assertFalse(prestamo.esta_activo())

    def test_devolver_en_la_misma_fecha_del_prestamo_es_valido(self):
        prestamo = self._crear()
        prestamo.devolver(self.fecha)
        self.assertFalse(prestamo.esta_activo())
        self.assertEqual(prestamo.dias_retraso(), 0)

    def test_devolver_dos_veces_lanza_prestamo_invalido(self):
        prestamo = self._crear()
        prestamo.devolver(date(2026, 1, 10))
        with self.assertRaises(PrestamoInvalidoError):
            prestamo.devolver(date(2026, 1, 11))

    def test_devolver_antes_de_fecha_prestamo_lanza_value_error_y_sigue_activo(self):
        prestamo = self._crear()
        with self.assertRaises(ValueError):
            prestamo.devolver(date(2025, 12, 31))
        self.assertTrue(prestamo.esta_activo())
        self.assertIsNone(prestamo.fecha_devolucion)

    def test_devolver_con_fecha_invalida_lanza_value_error_y_sigue_activo(self):
        prestamo = self._crear()
        with self.assertRaises(ValueError):
            prestamo.devolver("2026-01-10")
        self.assertTrue(prestamo.esta_activo())
        self.assertIsNone(prestamo.fecha_devolucion)

    def test_propiedades_de_fechas_son_solo_lectura(self):
        prestamo = self._crear()
        with self.assertRaises(AttributeError):
            prestamo.fecha_limite = date(2026, 1, 20)

    def test_str_incluye_titulo_y_estado_activo(self):
        texto = str(self._crear())
        self.assertIn("Título", texto)
        self.assertIn("activo", texto)

    def test_str_incluye_estado_devuelto(self):
        prestamo = self._crear()
        prestamo.devolver(date(2026, 1, 10))
        self.assertIn("devuelto", str(prestamo))


if __name__ == "__main__":
    unittest.main()
