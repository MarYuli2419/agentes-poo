"""Pruebas de la clase Biblioteca."""

import unittest
from datetime import date

from src.biblioteca import Biblioteca
from src.excepciones import (
    BibliotecaError,
    EntidadNoEncontradaError,
    LibroNoDisponibleError,
    LimitePrestamosError,
    PrestamoInvalidoError,
)
from src.libro import Libro
from src.socio import Socio


class TestBiblioteca(unittest.TestCase):
    """Verifica la coordinación de libros, socios y préstamos."""

    def setUp(self):
        self.biblioteca = Biblioteca("Central")
        self.libro = Libro("L1", "Libro 1", "Autor 1", 2)
        self.otro_libro = Libro("L2", "Libro 2", "Autor 2", 1)
        self.socio = Socio("S1", "Ana", "ana@example.com")
        self.socio_limitado = Socio(
            "S2",
            "Luis",
            "luis@example.com",
            limite_prestamos=1,
        )
        self.biblioteca.registrar_libro(self.libro)
        self.biblioteca.registrar_libro(self.otro_libro)
        self.biblioteca.registrar_socio(self.socio)
        self.biblioteca.registrar_socio(self.socio_limitado)

    def test_constructor_nombre_valido_crea_biblioteca_vacia(self):
        biblioteca = Biblioteca("Nueva")
        self.assertEqual(biblioteca.nombre, "Nueva")
        self.assertEqual(biblioteca.libros, ())
        self.assertEqual(biblioteca.socios, ())
        self.assertEqual(biblioteca.prestamos, ())

    def test_constructor_nombre_vacio_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Biblioteca("   ")

    def test_constructor_nombre_no_texto_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Biblioteca(123)

    def test_registrar_libro_nuevo_lo_agrega_al_catalogo(self):
        nuevo = Libro("L3", "Libro 3", "Autor 3", 1)
        self.biblioteca.registrar_libro(nuevo)
        self.assertIs(self.biblioteca.buscar_libro("L3"), nuevo)
        self.assertIn(nuevo, self.biblioteca.libros)

    def test_registrar_libro_duplicado_lanza_value_error(self):
        duplicado = Libro("L1", "Otro título", "Otro autor", 1)
        with self.assertRaises(ValueError):
            self.biblioteca.registrar_libro(duplicado)

    def test_registrar_libro_tipo_invalido_lanza_value_error(self):
        with self.assertRaises(ValueError):
            self.biblioteca.registrar_libro("no es un libro")

    def test_registrar_socio_nuevo_lo_agrega_al_registro(self):
        nuevo = Socio("S3", "Marta", "marta@example.com")
        self.biblioteca.registrar_socio(nuevo)
        self.assertIs(self.biblioteca.buscar_socio("S3"), nuevo)
        self.assertIn(nuevo, self.biblioteca.socios)

    def test_registrar_socio_duplicado_lanza_value_error(self):
        duplicado = Socio("S1", "Otra Ana", "otra@example.com")
        with self.assertRaises(ValueError):
            self.biblioteca.registrar_socio(duplicado)

    def test_registrar_socio_tipo_invalido_lanza_value_error(self):
        with self.assertRaises(ValueError):
            self.biblioteca.registrar_socio("no es un socio")

    def test_buscar_libro_existente_devuelve_el_libro(self):
        self.assertIs(self.biblioteca.buscar_libro("L1"), self.libro)

    def test_buscar_libro_inexistente_lanza_entidad_no_encontrada(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.biblioteca.buscar_libro("NO-EXISTE")

    def test_buscar_socio_existente_devuelve_el_socio(self):
        self.assertIs(self.biblioteca.buscar_socio("S1"), self.socio)

    def test_buscar_socio_inexistente_lanza_entidad_no_encontrada(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.biblioteca.buscar_socio("NO-EXISTE")

    def test_prestar_libro_y_socio_validos_crea_prestamo_y_actualiza_estado(self):
        prestamo = self.biblioteca.prestar(
            "L1",
            "S1",
            date(2026, 1, 1),
        )
        self.assertIs(prestamo.libro, self.libro)
        self.assertIs(prestamo.socio, self.socio)
        self.assertEqual(prestamo.fecha_limite, date(2026, 1, 15))
        self.assertEqual(self.libro.ejemplares_disponibles, 1)
        self.assertIn(prestamo, self.socio.prestamos_activos)
        self.assertIn(prestamo, self.biblioteca.prestamos_activos())
        self.assertIn(prestamo, self.biblioteca.prestamos)

    def test_prestar_libro_inexistente_lanza_entidad_no_encontrada(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.biblioteca.prestar("NO-EXISTE", "S1")

    def test_prestar_socio_inexistente_lanza_entidad_no_encontrada(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.biblioteca.prestar("L1", "NO-EXISTE")

    def test_prestar_sin_ejemplares_disponibles_lanza_libro_no_disponible(self):
        self.biblioteca.prestar("L2", "S1", date(2026, 1, 1))
        with self.assertRaises(LibroNoDisponibleError):
            self.biblioteca.prestar("L2", "S2", date(2026, 1, 2))
        self.assertEqual(self.otro_libro.ejemplares_disponibles, 0)

    def test_prestar_al_alcanzar_limite_lanza_limite_prestamos(self):
        self.biblioteca.prestar("L2", "S2", date(2026, 1, 1))
        with self.assertRaises(LimitePrestamosError):
            self.biblioteca.prestar("L1", "S2", date(2026, 1, 2))
        self.assertEqual(self.libro.ejemplares_disponibles, 2)

    def test_prestar_mismo_libro_dos_veces_al_mismo_socio_lanza_prestamo_invalido(self):
        self.biblioteca.prestar("L1", "S1", date(2026, 1, 1))
        with self.assertRaises(PrestamoInvalidoError):
            self.biblioteca.prestar("L1", "S1", date(2026, 1, 2))
        self.assertEqual(self.libro.ejemplares_disponibles, 1)

    def test_prestar_respeta_multiples_ejemplares_disponibles(self):
        self.biblioteca.prestar("L1", "S1", date(2026, 1, 1))
        self.biblioteca.prestar("L1", "S2", date(2026, 1, 2))
        self.assertEqual(self.libro.ejemplares_disponibles, 0)
        self.assertEqual(len(self.biblioteca.prestamos_activos()), 2)

    def test_prestar_con_fecha_invalida_lanza_value_error_y_no_cambia_estado(self):
        with self.assertRaises(ValueError):
            self.biblioteca.prestar("L1", "S1", "2026-01-01")
        self.assertEqual(self.libro.ejemplares_disponibles, 2)
        self.assertEqual(self.biblioteca.prestamos_activos(), [])
        self.assertEqual(self.socio.prestamos_activos, ())

    def test_devolver_prestamo_activo_actualiza_estado_y_devuelve_retraso(self):
        prestamo = self.biblioteca.prestar(
            "L1",
            "S1",
            date(2026, 1, 1),
        )
        retraso = self.biblioteca.devolver(prestamo, date(2026, 1, 20))
        self.assertEqual(retraso, 5)
        self.assertFalse(prestamo.esta_activo())
        self.assertEqual(prestamo.fecha_devolucion, date(2026, 1, 20))
        self.assertEqual(self.libro.ejemplares_disponibles, 2)
        self.assertEqual(self.socio.prestamos_activos, ())
        self.assertEqual(self.biblioteca.prestamos_activos(), [])

    def test_devolver_a_tiempo_devuelve_cero(self):
        prestamo = self.biblioteca.prestar(
            "L1",
            "S1",
            date(2026, 1, 1),
        )
        retraso = self.biblioteca.devolver(prestamo, date(2026, 1, 15))
        self.assertEqual(retraso, 0)

    def test_devolver_prestamo_ajeno_lanza_prestamo_invalido(self):
        otra = Biblioteca("Otra")
        libro = Libro("X1", "Libro X", "Autor X", 1)
        socio = Socio("X1", "Xavier", "xavier@example.com")
        otra.registrar_libro(libro)
        otra.registrar_socio(socio)
        prestamo = otra.prestar("X1", "X1", date(2026, 1, 1))

        with self.assertRaises(PrestamoInvalidoError):
            self.biblioteca.devolver(prestamo)

    def test_devolver_prestamo_ya_devuelto_lanza_prestamo_invalido(self):
        prestamo = self.biblioteca.prestar(
            "L1",
            "S1",
            date(2026, 1, 1),
        )
        self.biblioteca.devolver(prestamo, date(2026, 1, 10))
        with self.assertRaises(PrestamoInvalidoError):
            self.biblioteca.devolver(prestamo, date(2026, 1, 11))

    def test_devolver_tipo_invalido_lanza_value_error(self):
        with self.assertRaises(ValueError):
            self.biblioteca.devolver("no es un préstamo")

    def test_devolver_con_fecha_anterior_al_prestamo_no_cambia_estado(self):
        prestamo = self.biblioteca.prestar(
            "L1",
            "S1",
            date(2026, 1, 10),
        )
        with self.assertRaises(ValueError):
            self.biblioteca.devolver(prestamo, date(2026, 1, 9))
        self.assertTrue(prestamo.esta_activo())
        self.assertEqual(self.libro.ejemplares_disponibles, 1)
        self.assertIn(prestamo, self.socio.prestamos_activos)

    def test_prestamos_activos_solo_incluye_no_devueltos(self):
        prestamo_1 = self.biblioteca.prestar(
            "L1",
            "S1",
            date(2026, 1, 1),
        )
        prestamo_2 = self.biblioteca.prestar(
            "L2",
            "S2",
            date(2026, 1, 10),
        )
        self.biblioteca.devolver(prestamo_1, date(2026, 1, 10))
        self.assertEqual(self.biblioteca.prestamos_activos(), [prestamo_2])

    def test_prestamos_vencidos_incluye_solo_activos_con_retraso(self):
        prestamo_1 = self.biblioteca.prestar(
            "L1",
            "S1",
            date(2026, 1, 1),
        )
        prestamo_2 = self.biblioteca.prestar(
            "L2",
            "S2",
            date(2026, 1, 10),
        )
        self.assertEqual(
            self.biblioteca.prestamos_vencidos(date(2026, 1, 20)),
            [prestamo_1],
        )
        self.biblioteca.devolver(prestamo_1, date(2026, 1, 20))
        self.assertEqual(
            self.biblioteca.prestamos_vencidos(date(2026, 1, 24)),
            [],
        )
        self.assertEqual(
            self.biblioteca.prestamos_vencidos(date(2026, 1, 25)),
            [prestamo_2],
        )

    def test_prestamos_vencidos_sin_prestamos_devuelve_lista_vacia(self):
        self.assertEqual(self.biblioteca.prestamos_vencidos(), [])

    def test_historial_socio_incluye_prestamos_activos_y_devueltos(self):
        prestamo_1 = self.biblioteca.prestar(
            "L1",
            "S1",
            date(2026, 1, 1),
        )
        prestamo_2 = self.biblioteca.prestar(
            "L2",
            "S1",
            date(2026, 1, 2),
        )
        self.biblioteca.devolver(prestamo_1, date(2026, 1, 10))
        self.assertEqual(
            self.biblioteca.historial_socio("S1"),
            [prestamo_1, prestamo_2],
        )
        self.assertEqual(self.biblioteca.historial_socio("S2"), [])

    def test_historial_socio_inexistente_lanza_entidad_no_encontrada(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.biblioteca.historial_socio("NO-EXISTE")

    def test_libros_disponibles_excluye_libros_sin_ejemplares(self):
        prestamo = self.biblioteca.prestar(
            "L2",
            "S1",
            date(2026, 1, 1),
        )
        disponibles = {
            libro.isbn for libro in self.biblioteca.libros_disponibles()
        }
        self.assertEqual(disponibles, {"L1"})

        self.biblioteca.devolver(prestamo, date(2026, 1, 10))
        disponibles = {
            libro.isbn for libro in self.biblioteca.libros_disponibles()
        }
        self.assertEqual(disponibles, {"L1", "L2"})

    def test_propiedades_libros_socios_prestamos_son_tuplas_inmutables(self):
        self.assertIsInstance(self.biblioteca.libros, tuple)
        self.assertIsInstance(self.biblioteca.socios, tuple)
        self.assertIsInstance(self.biblioteca.prestamos, tuple)
        with self.assertRaises(AttributeError):
            self.biblioteca.libros = ()

    def test_errores_de_negocio_heredan_de_biblioteca_error(self):
        for excepcion in (
            EntidadNoEncontradaError,
            LibroNoDisponibleError,
            LimitePrestamosError,
            PrestamoInvalidoError,
        ):
            self.assertTrue(issubclass(excepcion, BibliotecaError))

        with self.assertRaises(BibliotecaError):
            self.biblioteca.buscar_libro("NO-EXISTE")

    def test_str_incluye_nombre_y_conteos(self):
        self.biblioteca.prestar("L1", "S1", date(2026, 1, 1))
        texto = str(self.biblioteca)
        self.assertIn("Central", texto)
        self.assertIn("2 libros", texto)
        self.assertIn("2 socios", texto)
        self.assertIn("préstamos activos", texto)


if __name__ == "__main__":
    unittest.main()
