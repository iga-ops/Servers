import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_sprawdz_kolejnosc_listy(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1), Product('AC10', 5)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual([Product('PP235', 1), Product('PP234', 2), Product('AC10', 5)], entries)

    def test_sprawdz_czy_blad(self):
        products = [Product('PN12', 3), Product('PP234', 2), Product('PP235', 1), Product('AC10', 5)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                entries = server.get_entries(2)

    def test_sprawdz_czy_pusta_lista(self):
        products = [Product('PN12', 1), Product('PP234', 2), Product('PP235', 1), Product('AC10', 5)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(1)
            self.assertEqual([], entries)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_sprawdz_dla_pustej(self):
        products = [Product('PN12', 1), Product('PP234', 2), Product('PP235', 1), Product('AC10', 5), Product('AMN32', 2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(1))

    def test_sprawdz_dla_za_duzej_listy(self):
        products = [Product('PN12', 1), Product('PP234', 2), Product('PP235', 1), Product('AC10', 5), Product('AMN32', 2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))


if __name__ == '__main__':
    unittest.main()
