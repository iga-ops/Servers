from abc import ABC, abstractmethod
from typing import List
from typing import Optional
from copy import deepcopy
import re


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __hash__(self):
        return hash((self.name, self.price))

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price


class Server(ABC):
    n_max_returned_entries = 3

    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_entries(self, n_letters: Optional[int]) -> List[Product]:
        pass


class ListServer(Server):

    def __init__(self, productlist: List[Product]):
        super().__init__()
        self.products = deepcopy(productlist)

    def get_entries(self, n_letters: Optional[int] = None) -> List[Product]:
        if n_letters is None:
            n_letters = 1

        new_list = []

        for el in self.products:
            if re.match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), el.name):
                new_list.append(el)

        if len(new_list) <= self.n_max_returned_entries:
            second_list = sorted(new_list, key=lambda el: el.price)
            return second_list
        else:
            raise TooManyProductsFoundError


class MapServer(Server):
    def __init__(self, productlist: List[Product]):
        super().__init__()
        productdict = dict()
        for el in productlist:
            productdict[el.name] = el
        self.products = deepcopy(productdict)

    def get_entries(self, n_letters: Optional[int] = None) -> List[Product]:
        if n_letters is None:
            n_letters = 1

        new_list = []

        for el in self.products.values():
            if re.match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), el.name):
                new_list.append(el)

        if len(new_list) <= self.n_max_returned_entries:
            second_list = sorted(new_list, key=lambda el: el.price)
            return second_list
        else:
            raise TooManyProductsFoundError


class Client:

    def __init__(self, city_centre: Server):
        self.city_server = city_centre

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            sum = 0
            koszyk = self.city_server.get_entries(n_letters)
            if len(koszyk) == 0:
                return None
            for el in koszyk:
                sum = sum + el.price
            return sum
        except TooManyProductsFoundError:
            return None


class ServerError(Exception):
    pass


class TooManyProductsFoundError(ServerError):
    pass

