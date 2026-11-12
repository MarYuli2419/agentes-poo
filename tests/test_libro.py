"""Pruebas de la clase Libro."""

import unittest

from src.excepciones import LibroNoDisponibleError, PrestamoInvalidoError
from src.libro import Libro


class TestLibro(unittest.TestCase):
    """Verifica la creación y el control de ejemplares de un libro."""

    def test_constructor_datos_validos_crea_libro_con_ejemplares_disponibles(self):
        libro = Libro(
            "978-1",
            "Cien años de soledad",
            "Gabriel García Márquez",
            3,
        )
        self.assertEqual(libro.isbn, "978-1")
        self.assertEqual(libro.titulo, "Cien años de soledad")
        self.assertEqual(libro.autor, "Gabriel García Márquez")
        self.assertEqual(libro.ejemplares_totales, 3)
        self.assertEqual(libro.ejemplares_disponibles, 3)
        self.assertTrue(libro.hay_disponible())

    def test_constructor_sin_ejemplares_explicitos_usa_uno_por_defecto(self):
        libro = Libro("978-1", "Título", "Autor")
        self.assertEqual(libro.ejemplares_totales, 1)
        self.assertEqual(libro.ejemplares_disponibles, 1)

    def test_constructor_isbn_vacio_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Libro("", "Título", "Autor")

    def test_constructor_titulo_solo_espacios_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Libro("978-1", "   ", "Autor")

    def test_constructor_autor_vacio_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Libro("978-1", "Título", "")

    def test_constructor_ejemplares_cero_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Libro("978-1", "Título", "Autor", 0)

    def test_constructor_ejemplares_negativos_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Libro("978-1", "Título", "Autor", -1)

    def test_constructor_ejemplares_no_entero_lanza_value_error(self):
        with self.assertRaises(ValueError):
            Libro("978-1", "Título", "Autor", "2")

    def test_prestar_ejemplar_con_disponibles_descuenta_uno(self):
        libro = Libro("978-1", "Título", "Autor", 2)
        libro.prestar_ejemplar()
        self.assertEqual(libro.ejemplares_disponibles, 1)

    def test_prestar_ejemplar_sin_disponibles_lanza_libro_no_disponible(self):
        libro = Libro("978-1", "Título", "Autor", 1)
        libro.prestar_ejemplar()
        with self.assertRaises(LibroNoDisponibleError):
            libro.prestar_ejemplar()
        self.assertEqual(libro.ejemplares_disponibles, 0)

    def test_devolver_ejemplar_prestado_incrementa_disponibles(self):
        libro = Libro("978-1", "Título", "Autor", 2)
        libro.prestar_ejemplar()
        libro.devolver_ejemplar()
        self.assertEqual(libro.ejemplares_disponibles, 2)

    def test_devolver_ejemplar_sin_prestamo_activo_lanza_prestamo_invalido(self):
        libro = Libro("978-1", "Título", "Autor", 2)
        with self.assertRaises(PrestamoInvalidoError):
            libro.devolver_ejemplar()
        self.assertEqual(libro.ejemplares_disponibles, 2)

    def test_devolver_ejemplar_mas_veces_que_prestamos_lanza_prestamo_invalido(self):
        libro = Libro("978-1", "Título", "Autor", 1)
        libro.prestar_ejemplar()
        libro.devolver_ejemplar()
        with self.assertRaises(PrestamoInvalidoError):
            libro.devolver_ejemplar()

    def test_hay_disponible_sin_ejemplares_libres_es_false(self):
        libro = Libro("978-1", "Título", "Autor", 1)
        libro.prestar_ejemplar()
        self.assertFalse(libro.hay_disponible())

    def test_propiedades_de_ejemplares_son_solo_lectura(self):
        libro = Libro("978-1", "Título", "Autor", 1)
        with self.assertRaises(AttributeError):
            libro.ejemplares_disponibles = 5

    def test_str_incluye_titulo_y_disponibilidad(self):
        libro = Libro("978-1", "Título", "Autor", 2)
        texto = str(libro)
        self.assertIn("Título", texto)
        self.assertIn("2/2 disponibles", texto)


if __name__ == "__main__":
    unittest.main()
