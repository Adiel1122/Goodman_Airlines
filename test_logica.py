"""
test_logica.py

Pruebas básicas para el módulo logica.py de Goodman Airlines.
Se ejecuta con: python test_logica.py
"""

import unittest
from logica import consultar_disponibilidad, comparar_precios, crear_reserva

class TestLogica(unittest.TestCase):

    def setUp(self):
        # Simulación de vuelos
        self.vuelos = [
            {
                "id": "V001",
                "origen": "CDMX",
                "destino": "NYC",
                "fecha": "2024-07-10 08:00",
                "precio": 3500.0,
                "asientos_disponibles": [{"codigo": "A1", "precio": 3500.0}]
            },
            {
                "id": "V002",
                "origen": "CDMX",
                "destino": "NYC",
                "fecha": "2024-07-10 12:00",
                "precio": 3200.0,
                "asientos_disponibles": [{"codigo": "B2", "precio": 3200.0}]
            },
            {
                "id": "V003",
                "origen": "CDMX",
                "destino": "LAX",
                "fecha": "2024-07-10 09:00",
                "precio": 4000.0,
                "asientos_disponibles": [{"codigo": "C3", "precio": 4000.0}]
            },
        ]
        self.usuario = {
            "usuario": "juan",
            "contraseña": "1234"
        }

    def test_consultar_disponibilidad(self):
        # Busca vuelos CDMX -> NYC en fecha exacta
        resultados = consultar_disponibilidad(self.vuelos, "CDMX", "NYC", "2024-07-10")
        self.assertEqual(len(resultados), 2)
        for vuelo in resultados:
            self.assertEqual(vuelo["origen"], "CDMX")
            self.assertEqual(vuelo["destino"], "NYC")
            self.assertTrue(vuelo["fecha"].startswith("2024-07-10"))
        
        # Busca vuelos inexistentes
        resultados = consultar_disponibilidad(self.vuelos, "CDMX", "MIA", "2024-07-10")
        self.assertEqual(len(resultados), 0)

    def test_comparar_precios(self):
        mas_barato = comparar_precios(self.vuelos)
        self.assertIsNotNone(mas_barato)
        self.assertEqual(mas_barato["id"], "V002")
        self.assertEqual(mas_barato["precio"], 3200.0)
        
        # Lista vacía devuelve None
        self.assertIsNone(comparar_precios([]))

    def test_crear_reserva(self):
        vuelo = self.vuelos[1]  # V002
        asiento = "B2"
        reserva = crear_reserva(self.usuario, vuelo, asiento)
        self.assertIn("id_reserva", reserva)
        self.assertEqual(reserva["usuario"], self.usuario["usuario"])
        self.assertEqual(reserva["vuelo_id"], "V002")
        self.assertEqual(reserva["origen"], "CDMX")
        self.assertEqual(reserva["destino"], "NYC")
        self.assertEqual(reserva["fecha"], "2024-07-10 12:00")
        self.assertEqual(reserva["asiento"], "B2")
        self.assertEqual(reserva["precio"], 3200.0)
        self.assertIn("fecha_reserva", reserva)

if __name__ == "__main__":
    unittest.main()